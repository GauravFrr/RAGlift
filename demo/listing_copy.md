# Gumroad & Whop Listing Copy — RAGLift 🚀

## Product Title
**RAGLift — Production RAG Starter Kit (Hybrid Search + RRF + Cross-Encoder Reranking)**

## Subtitle / Tagline
Stop losing search recall in your RAG app. Boost top-1 retrieval recall from 75.0% to 87.5% (100% Recall@5, 0.931 MRR) in under 5 minutes with a clean, self-hostable FastAPI + ChromaDB + BM25 stack.

## Price
**$49 (One-Time Purchase)** — Includes Single-Use Commercial License for personal and client projects.

---

## Sales Page Copy

### ❌ The Problem with Naive RAG Vector Search
You built a RAG chatbot or document search engine using naive cosine similarity vectors. At first, it looks great—until real users start asking specific questions:
- They search for exact error codes (`ERR_AUTH_001`), function names, or SKUs — and vector search returns completely irrelevant paragraphs.
- Answers are inconsistent because true target chunks are buried at rank #15 or #30.
- You have no benchmark script to prove whether prompt tweaks or chunking changes actually improve retrieval accuracy.

Fixing this properly takes weeks of reading papers on Reciprocal Rank Fusion (RRF) and fine-tuning cross-encoders.

---

### ✅ The Solution: RAGLift
**RAGLift** is a sellable, self-hostable RAG retrieval engine packaged into a clean, layered FastAPI service.

It combines:
1. **BM25 Keyword Search:** Instant exact token matching for codes, acronyms, and technical terms.
2. **Dense Vector Search:** Deep semantic intent matching via Gemini `text-embedding-004` (swappable to OpenAI or local models).
3. **Reciprocal Rank Fusion (RRF):** Mathematically fuses keyword and vector rank lists without score normalization bias.
4. **Cross-Encoder Reranking (`ms-marco-MiniLM-L-6-v2`):** Transformer self-attention re-scores top candidates, placing the true answer at Rank #1.
5. **Standalone Eval Suite (`eval/run_eval.py`):** Measure Recall@1, Recall@5, and MRR on your own document corpus out of the box.

---

### 📦 What's Inside the Download?
- **Complete Layered Source Code:** Clean `app/core`, `app/services`, `app/api/v1`, `app/retrieval` structure.
- **Standalone Eval Benchmark:** `python eval/run_eval.py` outputs a before/after recall comparison table.
- **One-Command Docker Setup:** `docker-compose up --build` brings up API + persistent ChromaDB.
- **CLI Ingestion Utilities:** `scripts/ingest_cli.py` and `scripts/reset_index.py`.
- **Single-Use Commercial License (`LICENSE.md`):** Use and deploy inside your own products and client deliverables.

---

## 📅 7-Day Distribution & Outreach Plan

| Day | Platform | Action | Target Audience |
|---|---|---|---|
| **Day 1** | Twitter/X | Post launch thread with before/after recall screenshot + 2-min demo video. | Indie hackers, AI devs |
| **Day 2** | Reddit | Share post on r/LangChain & r/MachineLearning: *"Why vector search alone fails for RAG (and how RRF + Cross-Encoder reranking fixes it)"*. | ML practitioners, RAG builders |
| **Day 3** | Discords | Post benchmark findings & GitHub repo link in LlamaIndex & LangChain Discord `#tools`/`#showcase` channels. | Developer communities |
| **Day 4** | Twitter/X | Search keywords *"RAG recall"*, *"vector search bad"*, *"hybrid search"* -> reply with benchmark insights + link. | Active buyers |
| **Day 5** | Hacker News | Show HN post: *"RAGLift — Self-hostable hybrid RAG retrieval kit with built-in recall benchmark"*. | Tech community |
| **Day 6** | IndieHackers | Article: *"How I packaged hybrid retrieval into a $49 starter kit"*. | Founders & freelancers |
| **Day 7** | Twitter/X | Post 1-week launch recap + case study comparing baseline vs reranked recall scores. | Retargeting audience |
