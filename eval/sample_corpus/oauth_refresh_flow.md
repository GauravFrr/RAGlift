# Background Token Refresh & Token Rotation

Access tokens automatically expire after 3600 seconds (1 hour). To maintain continuous session access without prompting the user to re-authenticate, your client application should execute a refresh flow.

Send a POST request to `/oauth/v2/token` with:
- `grant_type`: Set to `refresh_token`.
- `refresh_token`: The refresh token received during initial authorization.

CloudScale uses strict token rotation: every time a refresh token is presented, a new access token and a new refresh token are returned, invalidating the previous refresh token.
