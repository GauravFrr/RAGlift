# Global Rate Limiting Policy & Account Tiers

CloudScale limits request volume per minute based on account subscription tier:

- Free Tier: 60 requests per minute (RPM)
- Developer Tier: 1,000 requests per minute (RPM)
- Enterprise Tier: 10,000 requests per minute (RPM)

Rate limits are evaluated across rolling 60-second sliding windows.
