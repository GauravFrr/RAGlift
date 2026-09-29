# OAuth2 Token Exchange Protocol

To exchange a temporary authorization code for an API access token, issue a POST request to `/oauth/v2/token`.

Required Request Body:
- `grant_type`: Must be set to `authorization_code`.
- `code`: The authorization code received from the user redirect callback.
- `client_id`: Your application client ID.
- `client_secret`: Your confidential application client secret.

Upon validation, the service returns a JSON payload containing `access_token`, `refresh_token`, `expires_in` (seconds), and `token_type`.
