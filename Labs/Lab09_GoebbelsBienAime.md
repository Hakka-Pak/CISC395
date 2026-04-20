# Lab 09: RAG — Search Your Travel Guides

**Course:** CISC 395 Applied Generative AI and LLM Applications
**Week:** 10
**Points:** 100

---

## Overview

Right now, option `[6] Ask AI` answers from the LLM's general training data. This week you add **RAG (Retrieval-Augmented Generation)**: put your own travel guides in a folder, and the app automatically searches them before answering.

**What changes in `trip_notes/` this week:**

```
trip_notes/
├── guides/              ← NEW: add .txt, .md, or .pdf travel guides here
│   └── (sample files provided)
├── chroma_db/           ← auto-created when rag.py first runs
├── src/
│   ├── rag.py           ← NEW: index + search
│   ├── ai_assistant.py  ← add rag_ask()
│   ├── main.py          ← add [8] Search my guides, [R] Rebuild index
│   ├── models.py        (unchanged)
│   └── storage.py       (unchanged)
└── tests/
    └── check_rag_setup.py  ← NEW: verify packages
```

> **Tip:** `guides/` and `chroma_db/` both live at the `trip_notes/` root — not inside `src/` or `data/`.

---

## Prerequisites

- Lab 08 complete: `trip_notes/` with working `ask()` and menu options `[1]`–`[7]`
- `.venv` active, `.env` has `OPENROUTER_API_KEY`

---

## Setup

All steps run from **`trip_notes/`** with `.venv` active.

**Step 1 — Download this lab's files (from CISC395/ root):**

```bash
mkdir -p Labs/Lab09 && curl -o Labs/Lab09/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab09/setup.py && python Labs/Lab09/setup.py
```

> **Windows PowerShell (one line):**
> ```powershell
> New-Item -ItemType Directory -Force -Path Labs\Lab09; Invoke-WebRequest -Uri https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab09/setup.py -OutFile Labs\Lab09\setup.py; python Labs\Lab09\setup.py
> ```

→ Creates `trip_notes/guides/`, downloads prompt files and check script.

**Step 2 — Install new packages:**

```bash
cd trip_notes
pip install chromadb sentence-transformers pypdf
pip freeze > ../requirements.txt
```

> `sentence-transformers` downloads ~90 MB on first use (cached after that). `pypdf` adds PDF support.

**Step 3 — Verify setup:**

```bash
python tests/check_rag_setup.py
```

Expected output:
```
  ✓  chromadb installed
  ✓  sentence_transformers installed
  ✓  pypdf installed
  ✓  guides/ folder found (N files)
All checks passed.
```

**Commit:**
```bash
git add ../requirements.txt
git commit -m "chore: lab09 packages installed"
git push
```

---

## Exercises

---

### Exercise 1 — Explore and Add Guides (10 pts)

The `guides/` folder has sample travel guides provided by your instructor. Open it in VS Code Explorer and read a few.

Add **at least one guide of your own** — any destination you are interested in. Save it directly into `trip_notes/guides/` (the folder setup.py already created). Supported formats:

| Format | Notes |
|--------|-------|
| `.txt` | Plain text — simplest and most reliable |
| `.md`  | Markdown — treated as plain text |
| `.pdf` | Must be text-based (not a scanned image) |

You can write it yourself or use AI:
```
Write a 200-word destination guide for [City, Country] covering:
what it is like to visit, best season, 2–3 must-try foods,
2–3 activities, and 2 practical tips for a student traveler.
Plain text only, no headers.
Save the result as trip_notes/guides/[city_name].txt
```


**Your new guide:**

```
File: guides/[name].[ext]     Format: txt/md/pdf     Topic: [one line]
```

---

### Exercise 2 — Build `src/rag.py` (30 pts)

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code  (from trip_notes/)
@prompts/Lab09_Ex02_rag.md

# Option B — Copilot Chat sidebar
#file:trip_notes/prompts/Lab09_Ex02_rag.md
```

The AI will generate `src/rag.py` with:
- `build_index(force=False)` — reads all `.txt`, `.md`, `.pdf` files from `guides/`, chunks them (~200 words, 30-word overlap), embeds with `all-MiniLM-L6-v2`, stores in ChromaDB. Skips already-indexed chunks unless `force=True`.
- `search_guides(query, n_results=3)` — returns top matching text chunks
- `ensure_index()` — called by `search_guides()`: if `chroma_db/` is empty, automatically builds before searching and prints a message

**Run Terminal — build and test:**
```bash
python src/rag.py
```

Expected output:
```
Indexed N chunks from M files.

Indexed 101 chunks from 7 files.
```

**Paste your `src/rag.py`:**
```python
[import os
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
]
```

**Paste the build output:**
```
[e.g., Indexed 14 chunks from 3 files.]

--- Chunk 1 ---
since 1888. FOR WINE LOVERS The picturesque KOSHU VALLEY in Yamanashi Prefecture boasts some 70 wineries dotted across the landscape. The signature white wine made here is produced from the native Koshu grape; there is ample opportunity to sample it at the cellar doors located throughout the region.

--- Chunk 2 ---
AIDO Tohoku Above: Higashimokoto Shibazakura Park, Hokkaido. Below: Cherry blossom season at Tsuruga Castle in Fukushima Prefecture. JNTO2020p06_10_main_V8_MR_F.indd 7JNTO2020p06_10_main_V8_MR_F.indd 7 26/10/20 9:55 am26/10/20 9:55 am 6 The Luxury of Experience EXPLORE Experiencing Japan Japan has o

--- Chunk 3 ---
craftsmanship in abundance. • SENGAN-EN in Kagoshima Prefecture is the expansive estate of the Shimazu clan of samurai who ruled here during the Edo Period. Touring the traditional house and manicured gardens hint at the opulence of life for Japan’s ruling class in times gone by. • Kyushu boasts a n
```

**Understanding check — read `src/rag.py` before answering:**

1. Look at `chunk_text()`. Why does RAG split documents into chunks instead of sending the entire file to the LLM? (1–2 sentences)
2. Look at `build_index()`. What does `all-MiniLM-L6-v2` convert each chunk into, and why does ChromaDB store these instead of raw text? (2 sentences)

```text
1. RAG splits the document into chunks because the AI agent has context window limits and processing a large set of information can be risky and cost more, by chunking the system is able to find the and utilize the important information.

2. all-MiniLM-L6-v2 convert each chunk into a sequence of numbers called a vector.ChromaDB stores the vectors instead of raw data because they enable semantic similarity search which allows the retrieval that is based off meaning rather than the matching words.

```

**Commit:**
```bash
git add src/rag.py guides/
git commit -m "feat: rag index builder"
git push
```

---

### Exercise 3 — Test Search (15 pts)

Test `search_guides()` with three different queries. Run in **Run Terminal:**

```python
# Paste into python shell or save as a temp script
from src.rag import search_guides
chunks = search_guides("YOUR QUERY HERE", n_results=3)
for i, c in enumerate(chunks, 1):
    print(f"--- Chunk {i} ---")
    print(c[:300])
    print()
```

**Search 1 — a question answered by one of your guides:**
```
Query: [what are the best spots in NYC?]
Top chunk (first 60 words): [--- Chunk 1 ---
New York City, USA — Travel Guide New York City is made up of five boroughs: Manhattan, Brooklyn, Queens, the Bronx, and Staten Island. Most tourists spend the majority of their time in Manhattan and Brooklyn. The subway runs 24 hours a day and is the fastest way to get around — a single ride costs]
```

**Search 2 — a question that could span multiple guides:**
```
Query: [what is the best way to travel in japan?]
Top chunk (first 60 words): [Visiting Japan is a mesmerizing experience where ancient traditions seamlessly blend with futuristic innovation. The country is known for its meticulously organized society, bustling neon-lit cities, and serene landscapes, all underpinned by a culture of deep respect. The best season to visit is dur]
```

**Search 3 — a destination NOT in any of your guides:**
```
Query: [give me good places to visit in Cuba.]
Top chunk (first 60 words): [paste — what did ChromaDB return?]

in the city of Paris It takes its name after the confessor of Louis XIV, Jesuit Father Lachaise, who used to live on the site Napoleon established a cemetery here in 1804 after the city of Paris purchased the area Jim Morrison, the legendary singer of The Doors, is buried here (one of the reason for
```

**Understanding check:** For Search 3, ChromaDB returned something even though that destination is not in your guides. Why does this always happen? What should `rag_ask()` do to handle this gracefully? (2–3 sentences)

```text
ChromaDB returns the result that is nearest, meaning it looks for the closest vector even if it does not answer the question correctly, ChromaDB will provide a result. You can have rag_ask() to tell the AI to not answer if it does not have the correct information or answer.
```

---

### Exercise 4 — Connect RAG to the App (30 pts)

#### Part A — Add `rag_ask()` to `ai_assistant.py`

**AI (one line):**
```
# Option A
@prompts/Lab09_Ex04_ragask.md

# Option B
#file:trip_notes/prompts/Lab09_Ex04_ragask.md
```

`rag_ask(question)` should:
1. Call `search_guides(question, n_results=3)` — this auto-builds the index if needed
2. If no chunks returned: return a message telling the user to add guides and rebuild
3. Build a system prompt that instructs the LLM to answer **only** from the provided chunks
4. Call `ask()` with that system prompt and return the answer

#### Part B — Add menu options to `main.py`

**AI (one line):**
```
# Option A
@prompts/Lab09_Ex04_menu.md

# Option B
#file:trip_notes/prompts/Lab09_Ex04_menu.md
```

New menu options:
- `[8] Search my guides` — calls `rag_ask()`, prints the answer
- `[R] Rebuild search index` — calls `build_index(force=True)`, prints confirmation

**Run Terminal — test session:**

Run `python src/main.py` and test the following. Paste the full terminal output:

```
[Show:
 - Selecting [8] for the first time (should print "No index found. Building..." if chroma_db/ was empty)
 - A question answered from your guides
 - The same question using [6] Ask AI
 - Pressing [R] to rebuild the index]
```

**Compare:** What is different between the `[6]` answer and the `[8]` answer for the same question? (2–3 sentences)


```
comparing the answers from 6 and 8, 6 gave a thorough answer into different ways you can travel such as utilizing the train and having tickets that could easily help you get around, number 8 gives you information of how you can travel around japan and where you can get the resources in order to get around
```

**Understanding check:** You added a new file to `guides/` and tried option `[8]`. The answer didn't include information from the new file. Why? What do you do to fix it? (1–2 sentences)

```
The new file wasn't included because the ChromaDB search index was already built and doesn't automatically update the menu.
```

**Commit:**
```bash
git add src/rag.py src/ai_assistant.py src/main.py
git commit -m "feat: rag search integrated into menu"
git push
```

---

### Reflection (15 pts)

**1.** `.txt`, `.md`, and `.pdf` are all supported, but they are not equally reliable for RAG. What makes a document work well for indexing? What kind of PDF would fail silently and why? (2–3 sentences)

```
[Your answer]
```

**2.** The index is built from your `guides/` files and saved in `chroma_db/`. What happens if you delete a guide file but do not rebuild the index — will the old chunks still show up in search results? Is this a problem? (2–3 sentences)

```
[Your answer]
```

**3.** You now have two ways to ask questions: `ask()` (option `[6]`) and `rag_ask()` (option `[8]`). Describe a scenario where `rag_ask()` gives a *worse* answer than `ask()`. (2–3 sentences)

```
[Your answer]
```

---

## Submission

Submit **two things** on Blackboard:

1. **This `.md` file** with all exercises and reflections filled in
2. **Your CISC395 GitHub repository URL** — your instructor will verify `guides/` and commit history

**Paste your GitHub repository URL here:**
```
https://github.com/[your-username]/CISC395
```

Expected commits (in order):
```
chore: lab09 packages installed
feat: rag index builder
feat: rag search integrated into menu
```

---

## Grading Rubric

| Exercise | Criteria | Points |
|----------|---------|--------|
| Ex 1: Guides | 3+ files listed (incl. at least 1 your own), understanding check answered | 10 |
| Ex 2: rag.py | Code runs, index built, output pasted, understanding check answered | 30 |
| Ex 3: Search tests | 3 queries tested, chunks pasted, understanding check answered | 15 |
| Ex 4: Integration | `[8]` and `[R]` work, test session pasted, comparison answered, understanding check answered | 30 |
| Reflection | All 3 questions answered with substance | 15 |

**Understanding checks are required.** Empty answers lose those points.
**Commits are required.** Missing commits lose the commit portion of each exercise's points.

---

## Quick Reference

```bash
# Run the app
python src/main.py

# Test search directly
python -c "from src.rag import search_guides; [print(c[:200]) for c in search_guides('best food in tokyo')]"

# Force rebuild index (or press [R] in the menu)
python -c "from src.rag import build_index; build_index(force=True)"
```

**Next lab:** Lab 10 adds function calling — the AI will be able to run real tools (look up weather, calculate budgets) using the ReAct pattern.
