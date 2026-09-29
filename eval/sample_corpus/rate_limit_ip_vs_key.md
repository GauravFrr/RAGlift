# IP-Based vs Key-Based Throttling Rules

CloudScale applies distinct throttling mechanisms depending on authentication state:

- **Unauthenticated Public Endpoints:** Throttled strictly by client IPv4/IPv6 origin address (limit: 30 requests per minute per IP).
- **Authenticated Routes:** Throttled by API Key or OAuth Client ID across all client IPs (limit determined by your account subscription tier).

If multiple machines share a single API key, their combined request traffic counts against the single key quota.
