# Coding Style Guide
## Production RAG Starter Kit

This codebase will be read by a paying buyer trying to understand and extend it — readability is a product feature, not just a preference.

### 1. General
- Type hints on every function signature (params + return)
- Docstrings on every public function/class: what it does, not how (the "how" should be readable from the code itself)
- No magic numbers — every tunable value comes from `config.py` / `.env`, never hardcoded inline
- Pinned dependency versions in `requirements.txt` — no `>=` ranges

### 2. Naming
- Modules named by responsibility (`bm25.py`, `dense.py`, `fusion.py`, `reranker.py`), not generic (`utils.py`, `helpers.py`)
- Function names are verbs (`retrieve_hybrid`, `rerank_candidates`), not nouns

### 3. Comments — "why," not "what"
- The hybrid retrieval + RRF + reranking logic is the entire value proposition of this product. Every non-obvious decision there (why RRF over simple score averaging, why this specific reranker, why this top-k default) gets a short comment explaining the reasoning — a buyer paying for this should learn from reading it, not just run it.
- Skip comments that restate the code (`# increment counter` above `i += 1`)

### 4. Secrets & Config
- No API keys, tokens, or paths ever committed — `.env.example` only, real `.env` gitignored
- All config loaded through a single `config.py` — no scattered `os.getenv()` calls elsewhere

### 5. Logging
- Structured logging (not bare `print()`) for ingestion and query paths
- Log at INFO for request-level events, DEBUG for retrieval-internals (candidate counts, fusion scores)

### 6. Testing
- Lightweight smoke tests, not a full enterprise suite — this is a starter kit, not a client system
- Minimum coverage: ingestion succeeds end-to-end, `/query` returns results, eval script runs and produces a report without errors

### 7. Formatting
- `black` + `isort` defaults, no custom line-length overrides
- One class/major component per file — keep files buyers can read top-to-bottom in a few minutes
