# Rate Limit HTTP Response Headers

Every API response contains headers indicating your current request quota status:

- `X-RateLimit-Limit`: Maximum requests allowed in the current time window.
- `X-RateLimit-Remaining`: Remaining request allowance in the current window.
- `X-RateLimit-Reset`: Unix epoch timestamp (in seconds) when the current rate limit window resets.

Example:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1774528800
```
