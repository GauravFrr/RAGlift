# Database Backups & Point-In-Time Recovery (PITR)

CloudScale performs continuous write-ahead log (WAL) streaming and daily storage snapshots.

Point-In-Time Recovery (PITR):
- Allows restoring database state to any specific timestamp within your retention window (default 30 days).
- Useful if accidental data deletion or transaction corruption occurs.

Manual snapshots can be triggered anytime via CLI or API.
