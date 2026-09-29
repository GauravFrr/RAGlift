# Product Requirements Document
## Production RAG Starter Kit

### 1. Problem Statement
Most developers building RAG (Retrieval-Augmented Generation) applications ship naive vector-similarity search and hit a wall: retrieval recall is low, answers are inconsistent, and there's no clear next step. Fixing this properly (hybrid search + reranking, tuned and measured) normally takes weeks of research most indie devs and small teams don't have time for.

### 2. Product Summary
A production-grade, self-hostable RAG retrieval service that combines BM25 keyword search with dense vector search (Reciprocal Rank Fusion) and a cross-encoder reranker. Ships with a working demo corpus, a standalone evaluation script, and Docker one-command setup. Buyers can point it at their own documents and reproduce a measurable recall improvement.

### 3. Target Buyer
- Indie developers and freelancers building a RAG-based product (docs search, internal chatbot, support-ticket assistant, knowledge base Q&A)
- Small startups/teams who need a credible retrieval baseline without hiring an ML specialist
- Technical buyers comfortable with Python, Docker, and basic API integration

### 4. Goals
- Buyer can run the full stack locally in under 15 minutes (`docker-compose up`)
- Buyer can swap in their own corpus and re-run the eval script to see their own before/after recall numbers
- Buyer can integrate the `/query` endpoint into their own app without touching internals

### 5. Success Metrics (buyer-side)
- Time from download to first successful query: < 30 minutes
- Reproducible recall improvement on buyer's own labeled query set
- Zero required code changes to get the demo corpus running end-to-end

### 6. What's Included
- FastAPI retrieval service (ingestion + query endpoints)
- Hybrid retrieval: BM25 + dense embeddings, combined via Reciprocal Rank Fusion
- Cross-encoder reranker (ms-marco-MiniLM-L-6-v2) as the final reordering stage
- Standalone eval script with a sample labeled query set, producing a before/after recall report
- Docker Compose setup (API + vector store)
- `.env.example` for provider/config swapping (embedding provider, top-k values, reranker model)
- README with quickstart, architecture explanation, and API reference

### 7. Non-Goals
- Not a hosted/managed SaaS — this is self-hosted source code
- Not a fine-tuning or model-training product
- Not multi-language/multi-modal out of the box (text-only, English demo corpus)
- Not a no-code tool — buyer must be comfortable running Docker and editing `.env`

### 8. Pricing & Distribution
- Listed on Gumroad and Whop, $39–49 one-time
- Single-use commercial license per buyer (see `06_security_and_licensing.md`)

### 9. Support Scope
- README + inline code comments as primary support
- Best-effort email Q&A for setup issues within a defined window (see licensing doc)
- No custom integration work included
