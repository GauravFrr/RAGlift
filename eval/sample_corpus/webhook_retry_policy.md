# Webhook Retry Schedules & Delivery Durations

If your receiving endpoint returns a non-2xx HTTP status code or times out (10s threshold), CloudScale initiates automatic exponential backoff retries.

Retry Schedule:
- Retry 1: 30 seconds after initial failure.
- Retry 2: 5 minutes later.
- Retry 3: 30 minutes later.
- Retries continue exponentially for a maximum duration of 72 hours.

If your endpoint returns HTTP 200 or 204, delivery is marked successful and retries cease.
