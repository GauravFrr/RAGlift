# Technical Requirements Document
## Production RAG Starter Kit

### 1. Architecture Overview
```
                ┌─────────────────────┐
                │   FastAPI Service   │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌─────▼─────┐
   │ Ingest  │       │  Retrieve  │      │  Rerank   │
   │Pipeline │       │  (Hybrid)  │      │(cross-enc)│
   └────┬────┘       └─────┬─────┘      └─────┬─────┘
        │                  │                  │
   ┌────▼──────────────────▼──────────────────▼────┐
   │      BM25 index   +   ChromaDB (dense vectors)  │
   └──────────────────────────────────────────────────┘
```

### 2. Components

**Ingestion Service** (`app/services/ingestion_service.py`)
- Chunks input documents (configurable chunk size / overlap)
- Generates dense embeddings (default: Gemini `text-embedding-004`, swappable)
- Writes chunks to both the BM25 index and ChromaDB collection

**Hybrid Retrieval** (`app/retrieval/`)
- `bm25.py` — keyword search over the chunk corpus
- `dense.py` — vector similarity search via ChromaDB
- `fusion.py` — Reciprocal Rank Fusion (RRF) combining both result sets
- `reranker.py` — cross-encoder (`ms-marco-MiniLM-L-6-v2`) reorders the fused top-K candidates

Orchestrated by `app/services/retrieval_service.py`, which routes are kept thin against.

**API Layer** (`app/api/v1/`)
- `routes_ingest.py` — `POST /api/v1/ingest` (alias: `POST /ingest`), delegates to `ingestion_service`
- `routes_query.py` — `POST /api/v1/query` (alias: `POST /query`), delegates to `retrieval_service`, returns reranked top-N chunks
- `routes_health.py` — `GET /health` liveness check


**Eval Script** (`eval/run_eval.py`)
- Standalone, not exposed via API
- Takes a labeled query set (`eval/sample_queries.json`: query → relevant chunk IDs)
- Runs retrieval with and without reranking
- Outputs a before/after recall@k comparison table to stdout + a markdown report

### 3. Configuration (`.env`)
| Variable | Purpose | Default |
|---|---|---|
| `EMBEDDING_PROVIDER` | `gemini` / `openai` / `local` | `gemini` |
| `GEMINI_API_KEY` | API key for embeddings | — |
| `CHROMA_PATH` | Local persistence path | `./data/chroma` |
| `RERANKER_MODEL` | HuggingFace model name | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| `TOP_K_RETRIEVE` | Candidates before rerank | `50` |
| `TOP_K_RERANK` | Final results after rerank | `5` |
| `CHUNK_SIZE` | Ingestion chunk size (tokens) | `512` |
| `CHUNK_OVERLAP` | Ingestion chunk overlap | `50` |

### 4. Deployment
- `docker-compose.yml` runs two services: `api` (FastAPI) and `chromadb` (vector store)
- Single command: `docker-compose up --build`
- No external DB required beyond ChromaDB's own persistence

### 5. Extensibility Notes
- Embedding provider swap: implement `EmbeddingProvider` interface in `api/embeddings/`, set `EMBEDDING_PROVIDER`
- Corpus swap: drop documents into `data/corpus/`, run `/ingest` or the ingestion CLI
- Reranker swap: any HuggingFace cross-encoder checkpoint works via `RERANKER_MODEL`

### 6. Known Limitations (to disclose in README)
- Demo corpus and sample query set are small — buyer's own corpus size will affect absolute numbers, though the relative before/after lift is what's reproducible
- Reranking adds latency (cross-encoder inference on top-K candidates) — documented trade-off, not tunable away
- English-only tokenization for BM25 by default
