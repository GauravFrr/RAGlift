# Multi-Factor Authentication (MFA) Policy

Organization administrators can enforce mandatory Multi-Factor Authentication (MFA) across all team members.

When MFA enforcement is activated:
- Users without TOTP authenticator app or hardware security key setup will be blocked from accessing dashboard and CLI commands.
- API requests authenticated via personal developer access tokens remain functional, provided the account owner completed MFA verification within 30 days.
