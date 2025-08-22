# n8n-nodes-zadarma

Zadarma telephony API integration for n8n workflows.

## Installation

### From npm registry
```bash
npm install n8n-nodes-zadarma
```

### From GitHub Packages
```bash
npm install @zerox9dev/n8n-nodes-zadarma
```

Restart n8n, find **Zadarma** in node palette.

## Setup

```bash
# In n8n:
# 1. Credentials → Create New → Zadarma API
# 2. Enter API Key + Secret from https://my.zadarma.com/api/
# 3. Add Zadarma node to workflow
```

## Operations

- **Call Statistics** - Get call records for date range
- **Recording Download** - Get download link for call ID

## Usage

### Get Call Statistics
```json
{
  "resource": "statistics",
  "operation": "getStats", 
  "startDate": "2024-01-01T00:00:00Z",
  "endDate": "2024-01-02T00:00:00Z"
}
```

### Get Recording Link
```json
{
  "resource": "recording",
  "operation": "getLink",
  "callId": "pbx12345678"
}
```

## Features

- HMAC-SHA1 authentication
- RFC1738 URL encoding
- Sandbox/production modes
- Error handling with continue-on-fail

## Links

- [Zadarma API Docs](https://zadarma.com/en/support/api/)
- [GitHub](https://github.com/zerox9dev/zadarma-api)

## License

MIT License - see [LICENSE](LICENSE) file.