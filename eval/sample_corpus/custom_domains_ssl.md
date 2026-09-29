# Provisioning Custom Domains & Automatic TLS/SSL Certificates

Attach custom root domains or subdomains to hosted web deployments.

Steps:
1. Add CNAME record pointing `api.yourdomain.com` to `ingress.cloudscale.net`.
2. Register domain via CLI: `cloudscale domains add api.yourdomain.com`.

CloudScale automatically provisions and renews free Let's Encrypt TLS/SSL certificates.
