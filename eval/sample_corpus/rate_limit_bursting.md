# Token Bucket Algorithm & Burst Capacity

Rate limiting uses a leaky token bucket algorithm to accommodate short request spikes.

Token Bucket Rules:
- Buckets refill continuously at a steady token rate per second.
- Burst allowance allows clients to consume up to 2x your steady-state RPM for up to 10 seconds.
- Once burst tokens are exhausted, requests throttling engages until tokens refill.
