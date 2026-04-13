import os
from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

GUIDES_DIR = "guides"
DB_PATH = "chroma_db"
COLLECTION = "trip_guides"
CHUNK_SIZE = 200  # words
CHUNK_OVERLAP = 30  # words


def _get_embedder() -> SentenceTransformer:
    if not hasattr(_get_embedder, "_model"):
        _get_embedder._model = SentenceTransformer("all-MiniLM-L6-v2")
    return _get_embedder._model


def read_file(path: str) -> str:
    file_path = Path(path)

    try:
        ext = file_path.suffix.lower()
        if ext in {".txt", ".md"}:
            text = file_path.read_text(encoding="utf-8")
        elif ext == ".pdf":
            reader = PdfReader(str(file_path))
            text = "\n".join((page.extract_text() or "") for page in reader.pages)
        else:
            text = ""
    except Exception as error:
        print(f"Warning: could not read {file_path.name}: {error}")
        return ""

    if not text.strip():
        print(f"Warning: {file_path.name} has no extractable text (scanned PDF?), skipping.")
        return ""

    return text


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    if not words:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")
    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    step = chunk_size - overlap
    if step <= 0:
        raise ValueError("chunk_size must be greater than overlap.")

    chunks: list[str] = []
    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size]
        if not chunk_words:
            continue
        chunks.append(" ".join(chunk_words))

    return chunks


def build_index(force: bool = False):
    guides_path = Path(GUIDES_DIR)
    if not os.path.isdir(GUIDES_DIR):
        print("Error: guides/ folder not found.")
        return

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION)

    if force and collection.count() > 0:
        existing = collection.get()
        existing_ids = existing.get("ids", [])
        if existing_ids:
            collection.delete(ids=existing_ids)

    supported_exts = {".txt", ".md", ".pdf"}
    guide_files = sorted(
        file_path for file_path in guides_path.iterdir() if file_path.is_file() and file_path.suffix.lower() in supported_exts
    )

    if not guide_files:
        print("Warning: no supported files found in guides/.")
        return

    known_ids = set(collection.get().get("ids", [])) if collection.count() > 0 else set()
    embedder = _get_embedder()
    total_chunks_added = 0
    files_indexed = 0

    for file_path in guide_files:
        text = read_file(str(file_path))
        if not text:
            continue

        chunks = chunk_text(text)
        if not chunks:
            continue

        candidate_ids = [f"{file_path.stem}_chunk_{i}" for i in range(len(chunks))]
        to_add = [(chunk_id, chunk_text_value) for chunk_id, chunk_text_value in zip(candidate_ids, chunks) if force or chunk_id not in known_ids]

        if not to_add:
            continue

        ids_to_add = [item[0] for item in to_add]
        docs_to_add = [item[1] for item in to_add]
        vectors = embedder.encode(docs_to_add).tolist()
        collection.add(ids=ids_to_add, documents=docs_to_add, embeddings=vectors)

        known_ids.update(ids_to_add)
        total_chunks_added += len(ids_to_add)
        files_indexed += 1

    print(f"Indexed {total_chunks_added} chunks from {files_indexed} files.")


def ensure_index() -> object:
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION)
    if collection.count() == 0:
        print("No index found. Building from guides/...")
        build_index()
        collection = client.get_or_create_collection(name=COLLECTION)
    return collection


def search_guides(query: str, n_results: int = 3) -> list[str]:
    collection = ensure_index()
    total_docs = collection.count()
    if total_docs == 0:
        return []

    embedder = _get_embedder()
    vector = embedder.encode(query).tolist()
    n_results = min(n_results, total_docs)

    results = collection.query(query_embeddings=[vector], n_results=n_results)
    documents = results.get("documents", [])
    if not documents:
        return []
    return documents[0]


if __name__ == "__main__":
    build_index()
