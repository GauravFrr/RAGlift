# Handling Rate Limit Exceeded Errors (HTTP 429)

When your request throughput exceeds allowed rate quotas, the gateway responds with HTTP status 429 Too Many Requests.

Response Payload:
```json
{
  "error": "ERR_RATE_LIMIT_EXCEEDED",
  "detail": "Request quota exceeded. Retry after designated reset time."
}
```

Clients should inspect the `Retry-After` response header (specifying seconds to wait) and execute exponential backoff with random jitter.
