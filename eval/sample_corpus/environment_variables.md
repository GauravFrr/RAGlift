# Environment Variables & Encrypted Secrets Management

Inject configuration environment variables and encrypted secrets into running app instances.

Setting Variables via CLI:
`cloudscale env set DATABASE_URL="postgres://..." --env production`

Secrets are encrypted at rest using AES-256-GCM before being injected into container runtimes.
