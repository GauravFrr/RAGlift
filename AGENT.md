# AGENT.md — RAGLift Build Agent

You are building **RAGLift**, a sellable "Production RAG Starter Kit" (hybrid BM25+dense retrieval + cross-encoder reranking, packaged from the Retryv portfolio project for sale on Gumroad/Whop).

Before writing any code, read every file in `context/` in this order:
1. `01_PRD.md` — what this product is, who it's for, what's in/out of scope
2. `02_TRD.md` — architecture, config, API surface, known limitations
3. `03_backend_schema.md` — ChromaDB collection, BM25 index, ingestion log, eval query set formats
4. `07_folder_structure.md` — exact layered structure (`app/core`, `app/api/v1`, `app/schemas`, `app/services`, `app/embeddings`, `app/retrieval`) and the rationale for it
5. `04_implementation_plan.md` — phases in order (0, 0.5, 1–5), each with goal/tasks/files-touched/verification
6. `05_coding_style.md` — this codebase will be read by a paying buyer; readability is a product feature
7. `06_security_and_licensing.md` — what must never be committed, what the README must disclose
8. `08_dependencies.md` — the only approved packages, pinned exactly

## Hard Rules
- **Follow the file-touch map per phase.** Do not touch files outside a phase's declared scope, and do not start a phase before the previous one is verified per its own criteria in `04_implementation_plan.md`.
- **Layered structure is non-negotiable.** Routes (`app/api/v1/routes_*.py`) call into services (`app/services/*.py`) and contain no business logic themselves. If you find yourself writing retrieval/ingestion logic inside a route file, stop and move it.
- **Approved dependencies only**, versions pinned exactly as listed in `08_dependencies.md`. Adding anything not on that list requires a one-line justification recorded in `CHANGELOG.md` before use, not after.
- **Embedding provider must stay swappable.** Default is Gemini `text-embedding-004` via `app/embeddings/gemini_provider.py`, implementing the `EmbeddingProvider` interface in `app/embeddings/base.py`. Never hardcode a provider call outside that interface.
- **No secrets, ever.** Only `.env.example` with placeholder values is committed. Verify `.gitignore` excludes real `.env` and `data/` before every commit.
- **The eval script must run standalone.** `eval/run_eval.py` must never depend on the API server being up — it is the product's core trust signal (the 23%→84% recall claim) and must be independently verifiable by a skeptical buyer.
- **No portfolio/client residue.** This is a generic product now, not Retryv-the-portfolio-project. Any hardcoded corpus, personal API key, or "Gaurav's portfolio" branding found anywhere is a bug — remove it, don't work around it.
- **Structured-output-only for the eval report.** The before/after recall table must be generated from real measured numbers on the actual demo corpus run, never hardcoded or estimated — if a run fails, report the failure, don't fabricate a plausible-looking number.
- **Testing bar is "lightweight but real,"** per `05_coding_style.md`: `tests/unit/` covers fusion + reranker logic, `tests/integration/test_smoke.py` covers ingestion → query → eval end to end. Do not expand into a large enterprise suite — that's out of scope and wastes phase time.
- **Docs are binding, not aspirational.** If an implementation decision conflicts with something in `context/`, update the relevant doc in the same change — don't let code and docs drift apart.

## Phase Tracker
- [ ] Phase 0 — Strip & Generalize
- [ ] Phase 0.5 — Layered Structure Setup
- [ ] Phase 1 — Eval Script Productization
- [ ] Phase 2 — Dockerization
- [ ] Phase 3 — Documentation
- [ ] Phase 4 — Demo Recording
- [ ] Phase 5 — Listing & Launch

Check a box only once that phase's verification criterion in `04_implementation_plan.md` has actually been run and passed — not when the code merely looks done.