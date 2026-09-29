# Authentication Error Code Reference

HTTP 401 Unauthorized responses return a JSON payload with specific error codes:

- `ERR_AUTH_MISSING_HEADER`: The `Authorization` HTTP header was not included in the request.
- `ERR_AUTH_INVALID_SIGNATURE`: Token signature verification failed or token is malformed.
- `ERR_AUTH_EXPIRED_TOKEN`: The provided access token has expired and requires token refresh.
- `ERR_AUTH_INSUFFICIENT_SCOPE`: The API key lacks the required permission scope for this route.
