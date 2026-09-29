# Authentication & Security Overview

CloudScale APIs secure all incoming endpoint traffic using standard HTTP Authorization headers.
Supported authentication schemes include Bearer Tokens, API Keys, and OAuth2 access tokens.

To authenticate a request, include the token in the request header:
`Authorization: Bearer <your_api_token>`

All API requests must take place over HTTPS. Unencrypted HTTP requests are rejected immediately by the edge gateway before reaching your application services.
