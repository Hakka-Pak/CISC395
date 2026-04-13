from src.rag import search_guides
chunks = search_guides("YOUR QUERY HERE", n_results=3)
for i, c in enumerate(chunks, 1):
    print(f"--- Chunk {i} ---")
    print(c[:300])
    print()