# RAGLift Progress Tracking

## Executive Summary
- **Project Name:** RAGLift (Production RAG Starter Kit)
- **Current Task:** Resolved RRF Fusion Regression & Verified Monotonic Benchmark Performance.
- **Status:** 100% Complete & Fully Verified.

---

## Phase Checklist
- [x] **Phase 0 — Strip & Generalize**
- [x] **Phase 0.5 — Layered Structure Setup**
- [x] **Phase 1 — Eval Script Productization (Bug Fixed & Verified)**
  - Root Cause: `eval/run_eval.py` was falling back to `MockEmbeddingProvider` (pseudo-random SHA256 vectors), polluting the dense candidate list with random noise and diluting BM25 RRF ranks.
  - Fix: Implemented `LocalEmbeddingProvider` using `sentence-transformers` (`all-MiniLM-L6-v2`) for local vector embeddings when `GEMINI_API_KEY` is not present.
  - Verified Results (Zero Regressions across all stages):
    - Dense Only: Recall@1 = 75.0%, Recall@5 = 95.8%, MRR = 0.841
    - BM25 Only: Recall@1 = 75.0%, Recall@5 = 95.8%, MRR = 0.854
    - Hybrid (RRF): Recall@1 = 75.0%, Recall@5 = **100.0%**, MRR = **0.865**
    - Hybrid + Rerank: Recall@1 = **87.5%**, Recall@5 = **100.0%**, MRR = **0.931**
- [x] **Phase 2 — Dockerization**
- [x] **Phase 3 — Documentation**
  - Updated `README.md` hook line to reflect baseline BM25 Recall@1 (75.0%) vs Final Hybrid + Rerank Recall@1 (**87.5%**), Recall@5 (**100.0%**), and MRR (**0.931**).
- [x] **Phase 4 — Demo Recording**
  - Updated `demo/demo_script.md` with post-fix numbers.
- [x] **Phase 5 — Listing & Launch**
  - Updated `demo/listing_copy.md` with post-fix numbers.
