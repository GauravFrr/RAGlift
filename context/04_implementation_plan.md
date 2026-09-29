# Implementation Plan
## Production RAG Starter Kit — Packaging Phases

### Phase 0: Strip & Generalize
**Goal:** Remove everything specific to Retryv-as-portfolio-project; make it a clean, generic kit.
**Tasks:**
- Remove hardcoded FastAPI-docs corpus, personal API keys, portfolio branding/README
- Introduce `EmbeddingProvider` interface so the provider is swappable, not hardcoded
- Add `.env.example` covering every config value in the TRD table
**Files touched:** `app/core/config.py`, `app/embeddings/`, `.env.example`, delete old README/corpus
**Verification:** Fresh clone + `.env` fill-in runs with zero source edits

### Phase 0.5: Layered Structure Setup
**Goal:** Establish the routes/services/schemas separation before any other phase builds on it.
**Tasks:**
- Split existing route+logic code into `app/api/v1/routes_*.py` (thin) and `app/services/*.py` (logic)
- Add `app/schemas/` Pydantic models for request/response validation
- Add `app/core/logging.py` and `app/core/exceptions.py`
- Add `pyproject.toml` (black/isort/ruff), `Makefile`, `.github/workflows/ci.yml`
**Files touched:** `app/api/v1/`, `app/services/`, `app/schemas/`, `app/core/`, `pyproject.toml`, `Makefile`, `.github/workflows/ci.yml`
**Verification:** `make lint` and `make test` both pass; routes contain no business logic, only calls into services

### Phase 1: Eval Script Productization
**Goal:** Turn the internal 23%→84% measurement into a standalone, rerunnable feature.
**Tasks:**
- Extract eval logic into `eval/run_eval.py`, runnable independently of the API
- Ship a small demo corpus + `sample_queries.json` so it works out of the box
- Output a clear before/after recall@k table (stdout + markdown report file)
**Files touched:** `eval/run_eval.py`, `eval/sample_queries.json`, `eval/sample_corpus/`
**Verification:** `python eval/run_eval.py` produces a correct before/after table on the demo corpus

### Phase 2: Dockerization
**Goal:** Zero manual setup — one command to a working stack.
**Tasks:**
- `Dockerfile` for the API, `docker-compose.yml` wiring API + ChromaDB
- Healthcheck on `/health`, sane restart policy
**Files touched:** `Dockerfile`, `docker-compose.yml`
**Verification:** `docker-compose up --build` on a clean machine reaches a working `/query` endpoint

### Phase 3: Documentation
**Goal:** README that sells the value and gets a buyer to a working query in under 30 minutes.
**Tasks:**
- Hook line using the 23%→84% number
- Quickstart (Docker), architecture diagram, API reference, eval instructions
- Known Limitations section (honest, matches TRD section 6)
**Files touched:** `README.md`
**Verification:** A person with no prior context can follow it start to finish without asking a question

### Phase 4: Demo Recording
**Goal:** 2–3 minute proof video for the product listing.
**Tasks:**
- Script: quickstart → run eval script live → show before/after recall numbers on screen
- No narration padding — the numbers are the pitch
**Files touched:** `demo/demo_script.md`
**Verification:** Video is under 3 minutes and shows a real number change, not a mock

### Phase 5: Listing & Launch
**Goal:** Live on Gumroad + Whop with a distribution push, not a passive listing.
**Tasks:**
- Listing copy (problem-first, reuse structure that worked for the multi-agent kit)
- Set price ($39–49), attach `LICENSE.md`
- Daily distribution cadence: Twitter/X replies to RAG-recall complaints, r/LangChain, r/MachineLearning, LlamaIndex/LangChain Discords — same cadence as FlowPrecheck's outreach
**Files touched:** none (external listing + docs already produced)
**Verification:** Listing live, first outreach batch sent same day
