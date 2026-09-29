# Database Connection Pooling & Sizing Guidelines

Managed PostgreSQL databases feature integrated connection pooling powered by PgBouncer.

Recommended Connection Settings:
- Max Connections: Set client pool size to match instance vCPU count (e.g. 20 connections per vCPU).
- Pool Mode: `transaction` pooling recommended for stateless web microservices.
- Idle Timeout: Close connections idle for more than 300 seconds to free backend slots.

Improper pool sizing can exhaust backend database connections and degrade query response latency.
