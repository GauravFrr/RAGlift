# Official Node.js / TypeScript SDK Guide

Install via npm or yarn: `npm install @cloudscale/sdk`

Usage Example:
```typescript
import { CloudScale } from '@cloudscale/sdk';

const cloudscale = new CloudScale({ apiKey: process.env.CLOUDSCALE_API_KEY });
const webhooks = await cloudscale.webhooks.list();
```

Full TypeScript definitions included out of the box.
