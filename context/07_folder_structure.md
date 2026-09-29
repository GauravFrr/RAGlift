# Folder Structure
## Production RAG Starter Kit

### Why This Changed From v1
The first draft was flat (`api/main.py` doing everything). That's fine for a personal script, but a buyer evaluating "Production RAG Starter Kit" will read the structure as part of the quality signal. This version separates routes / business logic / data models — the standard layering buyers will recognize from real production FastAPI services — while staying light enough that `eval/`, `tests/`, and CI stay proportionate to a starter kit, not an enterprise app.

```
rag-starter-kit/
├── app/
│   ├── main.py                      # FastAPI app factory — mounts routers only, no logic
│   ├── core/
│   │   ├── config.py                 # Settings (pydantic-settings), single source of .env values
│   │   ├── logging.py                # Structured logging setup
│   │   └── exceptions.py             # Custom exceptions + FastAPI exception handlers
│   ├── api/
│   │   └── v1/
│   │       ├── routes_ingest.py       # POST /ingest — thin, calls ingestion_service
│   │       ├── routes_query.py        # POST /query — thin, calls retrieval_service
│   │       └── routes_health.py       # GET /health
│   ├── schemas/
│   │   ├── ingest.py                  # Pydantic request/response models
│   │   └── query.py
│   ├── services/
│   │   ├── ingestion_service.py        # Orchestrates chunk → embed → write (BM25 + Chroma)
│   │   └── retrieval_service.py        # Orchestrates hybrid retrieve → fuse → rerank
│   ├── embeddings/
│   │   ├── base.py                    # EmbeddingProvider interface
│   │   └── gemini_provider.py         # Default implementation, swappable
│   └── retrieval/
│       ├── bm25.py
│       ├── dense.py
│       ├── fusion.py                  # Reciprocal Rank Fusion
│       └── reranker.py                # Cross-encoder reranking
├── eval/
│   ├── run_eval.py                    # Standalone before/after recall script
│   ├── sample_queries.json
│   └── sample_corpus/
├── scripts/
│   ├── ingest_cli.py                   # Ingest from the command line, no API round-trip
│   └── reset_index.py                  # Wipe ChromaDB + BM25 index for a clean re-run
├── demo/
│   └── demo_script.md
├── tests/
│   ├── unit/
│   │   ├── test_fusion.py
│   │   └── test_reranker.py
│   └── integration/
│       └── test_smoke.py               # Ingestion → query → eval, end to end
├── data/                                # Gitignored — buyer's own corpus/index lands here
├── .github/
│   └── workflows/
│       └── ci.yml                       # Lint + smoke tests on every push
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
├── pyproject.toml                       # black/isort/ruff config, one source of truth
├── requirements.txt
├── Makefile                             # make up / make eval / make test shortcuts
├── CHANGELOG.md
├── LICENSE.md
└── README.md
```

### What Changed vs. v1
| Before | After | Why |
|---|---|---|
| `api/main.py` did routing + logic | `app/api/v1/routes_*.py` (thin) + `app/services/*.py` (logic) | Buyers extending this need to find "where do I add my own logic" fast — service layer is the answer, routes stay untouched |
| Config scattered | `app/core/config.py` + `app/core/logging.py` + `app/core/exceptions.py` | Groups app-wide concerns so buyers don't hunt across files |
| No CI | `.github/workflows/ci.yml` | Signals this is maintained like real software, not a one-off script dump — matches the bar set by other shipped projects |
| No lint/format config | `pyproject.toml` | One command (`make lint`) instead of buyers guessing formatting rules |
| Flat `tests/` | `tests/unit/` + `tests/integration/` | Matches the coding-style doc's "lightweight but real" testing bar — unit tests for the fusion/reranker logic buyers are paying to understand, one integration smoke test for the full path |
| No CLI utilities | `scripts/ingest_cli.py`, `scripts/reset_index.py` | Buyers swapping in their own corpus need to re-ingest/reset without touching the API — common first thing they'll want to do |
| No `Makefile` | `Makefile` | `make up`, `make eval`, `make test` — buyers shouldn't need to remember raw Docker/pytest commands |

### What Deliberately Did NOT Change
- No Postgres/SQL layer added — the backend schema doc's reasoning still holds; ChromaDB + flat files are enough, and adding a DB here would be complexity for its own sake
- `eval/` still sits outside `app/` — it's a selling feature (reproducible proof), not internal tooling, so it stays easy to find and run standalone
- Test suite stays "lightweight but real" per the coding style doc, not a full enterprise matrix — a starter kit doesn't need 90% coverage, it needs the reader to trust the core logic works
