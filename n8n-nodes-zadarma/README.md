# n8n-nodes-zadarma

**Zadarma API integration for n8n workflows**

[![npm version](https://badge.fury.io/js/n8n-nodes-zadarma.svg)](https://www.npmjs.com/package/n8n-nodes-zadarma)

## Installation

```bash
npm install n8n-nodes-zadarma
```

Restart n8n and the **Zadarma** node will appear in your palette.

## Setup

1. **Credentials** → **Create New** → **Zadarma API**
2. Enter API Key and Secret
3. Add Zadarma node to workflow
4. Select credentials and operation

## Operations

### Call Statistics
- Get call records for date range
- Returns: Call data with recording status

### Recording Download  
- Get download link for call ID
- Returns: Download URL

## Example

```json
{
  "name": "Get Calls",
  "type": "n8n-nodes-zadarma.zadarma",
  "parameters": {
    "resource": "statistics",
    "operation": "getStats",
    "startDate": "2024-01-01T00:00:00Z",
    "endDate": "2024-01-02T00:00:00Z"
  }
}
```

## Authentication

- HMAC-SHA1 signature generation
- RFC1738 URL encoding
- Automatic header injection

## Links

- **GitHub**: https://github.com/zerox9dev/zadarma-api
- **Zadarma API**: https://zadarma.com/en/support/api/

## Author

**zerox9dev** - Mirvald.vadim@icloud.com