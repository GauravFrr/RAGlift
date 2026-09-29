# RAGLift — Demo Video Script (2-3 Minutes)

## Video Objective
Show proof of value in under 3 minutes: standard vector retrieval vs. RAGLift's hybrid + cross-encoder pipeline, backed by live measured evaluation metrics.

---

## Scene Breakdown & Timing

| Scene | Duration | Visual Action | On-Screen Text / Voiceover |
|---|---|---|---|
| **Scene 1: The Problem** | 0:00 - 0:30 | Terminal showing standard vector search missing an exact keyword query (`ERR_AUTH_001` or SKU code). | *"Naive vector search fails when users search for exact terms, codes, or domain vocabulary. Retrieval recall stays stuck around ~23%."* |
| **Scene 2: One-Command Spin Up** | 0:30 - 1:00 | Terminal running `docker-compose up --build` followed by `curl http://localhost:8000/health`. | *"RAGLift is a production-grade, self-hostable RAG starter kit. Runs locally in under 60 seconds with Docker."* |
| **Scene 3: Live Ingestion & Search** | 1:00 - 1:45 | Ingest sample markdown docs via `python scripts/ingest_cli.py --path eval/sample_corpus/`. Send a `POST /api/v1/query` request in Postman/HTTPie. | *"Chunks documents, generates embeddings, builds BM25 index, and runs hybrid RRF fusion + Cross-Encoder reranking."* |
| **Scene 4: Standalone Eval Benchmark** | 1:45 - 2:30 | Terminal executing `python eval/run_eval.py`. Highlight the stdout ASCII comparison table. | *"Run `eval/run_eval.py` on your own corpus to see real measured recall improvements—taking your top-1 retrieval recall from 75.0% to 87.5% (100% Recall@5)."* |
| **Scene 5: Call to Action** | 2:30 - 2:45 | Show project repository structure & Gumroad listing link. | *"Self-hostable, clean layered architecture, single-use commercial license. Get RAGLift today."* |

---

## Screen Recording Commands (Copy-Paste Sequence)

```bash
# 1. Start the stack
docker-compose up --build -d

# 2. Check health status
curl http://localhost:8000/health

# 3. Run standalone evaluation benchmark
python eval/run_eval.py

# 4. View generated markdown report
cat eval/eval_report.md
```
