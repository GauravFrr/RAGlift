# Security & Licensing
## Production RAG Starter Kit

### 1. License Model
- Single-use commercial license per purchase: buyer may use, modify, and deploy the code in their own products (including client work)
- No resale or redistribution of the source code itself as a competing product/template
- No attribution required in buyer's shipped product
- Full license text delivered as `LICENSE.md` inside the package

### 2. Data & Privacy
- The kit does not transmit buyer data anywhere except the embedding provider the buyer configures (e.g., Gemini API) — documented explicitly in the README so buyers know what leaves their environment
- No telemetry, analytics, or phone-home behavior of any kind
- Buyer is responsible for compliance around any data they choose to ingest (PII, confidential docs, etc.) — stated plainly, not left implicit

### 3. Secrets Handling
- `.env.example` ships with placeholder values only, never real keys
- README explicitly warns against committing `.env` to version control

### 4. Support Window & Disclaimer
- Best-effort email support for setup/integration questions for 30 days post-purchase
- No SLA, no custom feature development included
- Sold "as-is" — no warranty of fitness for a specific buyer's production scale or data volume; the reproducible recall improvement applies to retrieval quality, not a guarantee of infrastructure-level performance at any scale

### 5. Why This Doc Exists
Selling code (vs. a SaaS) shifts trust and liability questions onto explicit terms instead of a live support relationship — this doc is what protects both the buyer's expectations and Gaurav's time once the kit is out in the world.
