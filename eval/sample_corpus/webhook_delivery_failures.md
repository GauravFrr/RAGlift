# Troubleshooting Webhook Delivery Failures & Auto-Disabling

If a webhook endpoint experiences 100 consecutive failed delivery attempts, the system automatically disables the endpoint subscription.

Error Status: `ERR_WEBHOOK_ENDPOINT_DISABLED`

Recovery Steps:
1. Fix your endpoint application server.
2. Verify endpoint accessibility using the dashboard webhook test ping utility.
3. Manually re-enable the endpoint in the Webhooks dashboard settings.
