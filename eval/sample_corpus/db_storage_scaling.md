# Automatic Storage Expansion & Disk Quotas

To prevent database write outages caused by full disks, CloudScale enables storage auto-scaling by default.

Auto-Scale Trigger:
- When remaining free disk storage falls below 10% of total provisioned capacity, disk size is automatically expanded by 20%.
- Storage auto-expansion occurs seamlessly without cluster reboot or query interruption.
