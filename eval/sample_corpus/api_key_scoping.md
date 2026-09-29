# API Key Permissions & Granular Scoping

Programmatic API keys can be restricted using fine-grained permission scopes to enforce the principle of least privilege.

Available Scopes:
- `read:analytics`: Query usage statistics and telemetry metrics.
- `write:webhooks`: Create, modify, or delete webhook event subscriptions.
- `read:billing`: View historical invoices and current usage meters.
- `admin:deploy`: Trigger deployment builds and manage production container instances.

Keys can be restricted at key creation time or updated in the security dashboard.
