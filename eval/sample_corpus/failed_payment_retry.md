# Failed Payment Retries & Dunning Process

If a recurring credit card transaction fails during renewal, CloudScale enters automated dunning management.

Dunning Schedule:
- Day 1: Automated email notification sent to billing contact; retry attempt 1.
- Day 3: Retry attempt 2.
- Day 7: Retry attempt 3; account warning banner displayed.
- Day 14: Final retry attempt; account suspended if unpaid.

Grace period remains active for 14 days before resource deprovisioning occurs.
