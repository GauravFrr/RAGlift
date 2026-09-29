# RAGLift Master Todo List

## Currently Doing
- [x] RRF Fusion Regression Debugged & Resolved!

## Completed Verification Items
- [x] **Check 1: RRF Formula & Rank Indexing** — Verified 1-indexed ranks and $1/(k + rank)$ formula ($k=60$).
- [x] **Check 2: Dense Retriever Embedding Quality** — Identified that missing API keys caused fallback to pseudo-random hash vectors in `MockEmbeddingProvider`. Built `LocalEmbeddingProvider` (`all-MiniLM-L6-v2`) for local real vector embeddings.
- [x] **Check 3: Document & Chunk ID Alignment** — Verified exact chunk ID alignment (`{doc_id}_0`) across BM25 and Dense storage.
- [x] **Check 4: Monotonic Benchmark Progression** — Verified that Hybrid (RRF) MRR (0.865) and Recall@5 (100%) improve over BM25 (0.854 / 95.8%), and Hybrid + Rerank further lifts Recall@1 to 87.5% and MRR to 0.931.
- [x] **Check 5: Copy & Documentation Alignment** — Updated `README.md`, `demo/listing_copy.md`, and `demo/demo_script.md` to compare the BM25 baseline (75.0% / 0.854) against Hybrid + Rerank (87.5% / 0.931).
