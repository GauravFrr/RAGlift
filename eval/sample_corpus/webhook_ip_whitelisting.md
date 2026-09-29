# Static IP Egress Whitelisting for Webhook Delivery

If your server infrastructure operates behind a strict inbound firewall, whitelist CloudScale's static egress IP blocks for webhook traffic:

- `198.51.100.10`
- `198.51.100.11`
- `198.51.100.12`

All webhook POST requests originate exclusively from these IP addresses.
