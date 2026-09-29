# Zero-Downtime Database Schema Migrations

Executing schema changes on live production databases requires backward-compatible migration steps.

Recommended Workflow:
1. Expand schema: Add new columns or tables as nullable or with defaults.
2. Deploy app code that writes to both old and new schema structures.
3. Backfill historical records asynchronously.
4. Contract schema: Remove deprecated columns in a subsequent deployment.
