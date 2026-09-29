# Official Python SDK (`cloudscale-py`) Guide

Install via pip: `pip install cloudscale-py`

Usage Example:
```python
from cloudscale import CloudScaleClient

client = CloudScaleClient(api_key="cs_live_12345")
response = client.webhooks.list()
print(response.data)
```

Handles automatic retries, rate limit backoff, and exception parsing.
