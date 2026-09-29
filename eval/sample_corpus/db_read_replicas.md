# Database Read Replicas & Scaling Read Workloads

Scale read-heavy database throughput by attaching asynchronous read replica nodes.

Replica Details:
- Supports up to 5 read replicas per primary database cluster.
- Asynchronous replication lag is typically under 50 milliseconds across local availability zones.
- Direct read queries to replica connection string: `postgres://user:pass@replica.db.cloudscale.net:5432/dbname`.
