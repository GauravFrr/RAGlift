# RAGLift — Production RAG Starter Kit 🚀

> **Boost your RAG application's top-1 retrieval recall from 75.0% to 87.5% (100% Recall@5, 0.931 MRR) using production-grade hybrid search (BM25 + vector similarity) with Reciprocal Rank Fusion (RRF) and Cross-Encoder reranking.**

---

## 💡 Why RAGLift?

Most teams building RAG applications ship naive vector-similarity search and hit a wall:
1. **Low Retrieval Recall:** Dense embeddings miss exact keyword matches like error codes, function signatures, function names, and SKUs.
2. **Rank Misalignment:** Vector distance scores do not map cleanly to answer quality.
3. **Lack of Measurement:** No baseline script to verify whether retrieval pipeline changes actually improve answer relevance.

**RAGLift fixes this out of the box.** It packages a multi-stage retrieval engine with a standalone evaluation benchmark, allowing you to prove measurable recall gains on your own document corpus.

---

## 🏗️ Architecture Overview

```
                          ┌─────────────────────┐
                          │   FastAPI Service   │
                          └──────────┬──────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
             ┌────▼────┐       ┌─────▼─────┐      ┌─────▼─────┐
             │ Ingest  │       │  Retrieve │      │  Rerank   │
             │Pipeline │       │  (Hybrid) │      │(cross-enc)│
             └────┬────┘       └─────┬─────┘      └─────┬─────┘
                  │                  │                  │
             ┌────▼──────────────────▼──────────────────▼────┐
             │      BM25 Index   +   ChromaDB (dense vectors) │
             └────────────────────────────────────────────────┘
```

### Retrieval Pipeline Stages:
1. **Keyword Search (BM25):** Fast exact-match retrieval capturing domain terms, codes, and exact tokens.
2. **Dense Vector Search (ChromaDB):** Semantic similarity matching powered by Gemini `text-embedding-004` or local SentenceTransformers (`all-MiniLM-L6-v2`).
3. **Reciprocal Rank Fusion (RRF):** Combines raw BM25 and vector rank lists using $RRF(d) = \sum \frac{1}{k + rank(d)}$ without raw score scale bias.
4. **Cross-Encoder Reranker (`ms-marco-MiniLM-L-6-v2`):** Transformer self-attention re-scores top candidates to push the true relevant chunk into Rank #1.

---

## 🚀 Quickstart (Under 5 Minutes)

### Option A: Docker Compose (Recommended)

1. **Clone & Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env and set your GEMINI_API_KEY (optional; defaults to local SentenceTransformer)
   ```

2. **Launch Services:**
   ```bash
   docker-compose up --build
   ```

3. **Verify Health:**
   ```bash
   curl http://localhost:8000/health
   # {"status":"ok","service":"RAGLift","version":"1.0.0"}
   ```

### Option B: Local Python Setup

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install pinned dependencies
pip install -r requirements.txt

# 3. Start API server
uvicorn app.main:app --reload --port 8000
```

---

## 📊 Standalone Evaluation Benchmark

RAGLift ships with a standalone evaluation engine that measures retrieval recall without needing the API server to be active. By default (or when `GEMINI_API_KEY` is not set), the benchmark runs deterministically using local SentenceTransformers (`all-MiniLM-L6-v2`) requiring **zero API keys** or cloud credentials.

Run the evaluation script on the sample demo corpus:
```bash
python eval/run_eval.py
```

### Sample Output:
```text
==========================================================================
                RAGLIFT RETRIEVAL EVALUATION REPORT                       
==========================================================================
Total Test Queries Evaluated: 24
Evaluation Horizon: Top-5 Chunks
--------------------------------------------------------------------------
Retrieval Pipeline Stage  | Recall@1   | Recall@5   | MRR     
--------------------------------------------------------------------------
Dense Only                |     75.0% |     95.8% |   0.841
BM25 Only                 |     75.0% |     95.8% |   0.854
Hybrid (RRF)              |     75.0% |    100.0% |   0.865
Hybrid + Rerank           |     87.5% |    100.0% |   0.931
==========================================================================
```

A detailed report is automatically written to `eval/eval_report.md`.

To evaluate your own domain corpus, place your documents in `eval/sample_corpus/` and update `eval/sample_queries.json` with ground-truth chunk IDs.

---

## ⚙️ Configuration Reference

All settings are configured via environment variables or `.env`:

| Variable | Purpose | Default |
|---|---|---|
| `EMBEDDING_PROVIDER` | Swappable provider (`gemini`, `openai`, `mock`) | `gemini` |
| `GEMINI_API_KEY` | Google Gemini API key | `""` |
| `CHROMA_PATH` | Persistence directory for ChromaDB vector store | `./data/chroma` |
| `BM25_INDEX_PATH` | Persistence path for serialized BM25 index | `./data/bm25_index.pkl` |
| `INGESTION_LOG_PATH` | Path for append-only ingestion audit log | `./data/ingestion_log.jsonl` |
| `RERANKER_MODEL` | HuggingFace cross-encoder model name | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| `TOP_K_RETRIEVE` | Candidates retrieved per search mode before fusion | `50` |
| `TOP_K_RERANK` | Top results returned after cross-encoder reranking | `5` |
| `CHUNK_SIZE` | Words/tokens per document chunk | `512` |
| `CHUNK_OVERLAP` | Overlapping words between consecutive chunks | `50` |
| `LOG_LEVEL` | Log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `INFO` |

---

## 📖 API Reference

### 1. Document Ingestion
**`POST /api/v1/ingest`**

Chunks input text, computes vector embeddings, and writes to both BM25 and ChromaDB storage.

**Request Payload:**
```json
{
  "documents": [
    {
      "doc_id": "auth_guide",
      "text": "All API requests require a Bearer token in the Authorization header.",
      "metadata": { "category": "security" }
    }
  ],
  "chunk_size": 512,
  "chunk_overlap": 50
}
```

**Response:**
```json
{
  "status": "success",
  "documents_processed": 1,
  "total_chunks": 1,
  "ingested_at": "2026-09-26T12:00:00+00:00"
}
```

### 2. Hybrid Query Search
**`POST /api/v1/query`**

Executes multi-stage hybrid retrieval (BM25 + Dense -> RRF Fusion -> Cross-Encoder Reranker).

**Request Payload:**
```json
{
  "query": "How do I authenticate requests?",
  "top_k_retrieve": 50,
  "top_k_rerank": 5,
  "use_reranker": true
}
```

**Response:**
```json
{
  "query": "How do I authenticate requests?",
  "results": [
    {
      "chunk_id": "auth_guide_0",
      "doc_id": "auth_guide",
      "text": "All API requests require a Bearer token in the Authorization header.",
      "score": 0.8924,
      "rank": 1,
      "metadata": {
        "source_path": "auth_guide",
        "ingested_at": "2026-09-26T12:00:00+00:00"
      }
    }
  ],
  "total_results": 1
}
```

### 3. Health Check
**`GET /health`**

Returns `{"status": "ok", "service": "RAGLift", "version": "1.0.0"}`.

---

## 🛠️ CLI Utilities

- **CLI Document Ingestion:**
  ```bash
  python scripts/ingest_cli.py --path /path/to/my_docs/
  ```
- **Reset Storage & Indexes:**
  ```bash
  python scripts/reset_index.py
  ```

---

## 🔌 Extensibility & Customization

### Swappable Embedding Providers
To implement a new provider (e.g., OpenAI, Cohere, local HuggingFace):
1. Subclass `EmbeddingProvider` in `app/embeddings/base.py`.
2. Implement `embed_documents(texts)` and `embed_query(text)`.
3. Register your provider in `app/embeddings/__init__.py`.

### Changing the Reranker Model
Set `RERANKER_MODEL` in your `.env` file to any HuggingFace Cross-Encoder model (e.g. `BAAI/bge-reranker-large`).

---

## 🔒 Security & Data Privacy

- **No Telemetry:** RAGLift contains zero tracking, phone-home, or analytical telemetry.
- **Data Boundary:** Document text is only sent to the embedding provider configured by you (e.g., Gemini API).
- **Secrets Management:** Real keys are never committed. Verify `.gitignore` excludes `.env` and `data/`.

---

## ⚠️ Known Limitations

1. **Latencies on Large candidate lists:** Cross-Encoder reranking performs transformer self-attention over candidate pairs. Keeping `TOP_K_RETRIEVE` around 50 balances top-tier recall with fast response times.
2. **English Tokenization Default:** BM25 uses standard whitespace and word tokenization tuned for English.
3. **Corpus Scale:** Benchmark statistics scale with corpus density; re-run `python eval/run_eval.py` on your own labeled dataset to establish custom recall gains.
4. **Small Cross-Encoder Domain Nuances:** Lightweight cross-encoders (`ms-marco-MiniLM-L-6-v2`) may occasionally prefer general keyword overlap on closely related topics (e.g., webhook security verification vs. webhook IP firewalling). For production domains requiring ultra-fine discrimination, configure a larger reranker model like `BAAI/bge-reranker-large` via `RERANKER_MODEL`.

---

## 📄 License
This starter kit is delivered under a **Single-Use Commercial License** (see `LICENSE.md`). You may use, modify, and deploy it inside your commercial projects and client deliverables.
