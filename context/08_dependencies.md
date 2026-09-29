# Dependencies
## Production RAG Starter Kit

Kept deliberately minimal — every added dependency is one more thing that can break on a buyer's machine.

| Package | Purpose |
|---|---|
| `fastapi` | API layer |
| `uvicorn` | ASGI server |
| `chromadb` | Vector store for dense retrieval |
| `rank-bm25` | BM25 keyword search |
| `sentence-transformers` | Cross-encoder reranker inference |
| `google-generativeai` | Default embedding provider (Gemini) — swappable |
| `python-dotenv` | `.env` loading |
| `pydantic` | Request/response schemas, config validation |
| `pytest` | Smoke tests |

### Rules
- All versions pinned exactly in `requirements.txt` (no `>=`) — reproducibility matters more than always having the latest patch for a product buyers will set up once and rarely touch again
- Any new dependency added post-launch needs a one-line justification in `CHANGELOG.md` — no silent additions
