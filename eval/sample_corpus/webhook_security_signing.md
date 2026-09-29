# Webhook Payload Verification & Signature Validation

To ensure incoming webhook HTTP requests originate from CloudScale and have not been tampered with by a malicious third party, verify the HMAC signature.

Verification Procedure:
1. Extract signature header `X-CloudScale-Signature`.
2. Compute HMAC-SHA256 digest using raw request body bytes and your webhook secret key.
3. Compare computed digest against signature header using constant-time string comparison.

Never process unverified webhook payloads in production.
