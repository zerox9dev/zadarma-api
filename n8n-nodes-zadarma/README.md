# n8n-nodes-zadarma

**Professional Zadarma API integration for n8n workflows**

This custom n8n node provides seamless integration with the Zadarma telephony platform, enabling automated call management and audio recording workflows.

[![npm version](https://badge.fury.io/js/n8n-nodes-zadarma.svg)](https://www.npmjs.com/package/n8n-nodes-zadarma)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Installation

### NPM Installation (Recommended)

```bash
npm install n8n-nodes-zadarma
```

### Manual Installation

1. Navigate to your n8n user directory:
   ```bash
   cd ~/.n8n/nodes
   ```

2. Install the package:
   ```bash
   npm install n8n-nodes-zadarma
   ```

3. Restart your n8n instance

4. The **Zadarma** node will appear in your node palette under **Communication**

---

## ⚙️ Configuration

### 1. Set up Zadarma API Credentials

1. Go to **Credentials** → **Create New**
2. Select **Zadarma API**
3. Enter your credentials:
   - **API Key**: Your Zadarma API key
   - **API Secret**: Your Zadarma API secret  
   - **Sandbox Mode**: Toggle for testing environment

### 2. Add Zadarma Node to Workflow

1. Drag the **Zadarma** node from the palette
2. Select your configured credentials
3. Choose the desired operation

---

## 📋 Available Operations

### 📊 Call Statistics

Retrieve call records for a specified date range.

**Parameters:**
- **Start Date**: Beginning of the time range (ISO format)
- **End Date**: End of the time range (ISO format)

**Returns:**
```json
{
  "status": "success",
  "stats": [
    {
      "call_id": "1234567890.12345",
      "callstart": "2024-01-01 10:30:00", 
      "disposition": "answered",
      "seconds": 125,
      "is_recorded": "true"
    }
  ]
}
```

### 🎵 Call Recording Download

Get download link for a specific call recording.

**Parameters:**
- **Call ID**: The unique identifier of the call

**Returns:**
```json
{
  "status": "success",
  "link": "https://download-url.zadarma.com/recording.mp3"
}
```

---

## 🔧 Example Workflows

### Basic Call Statistics Retrieval

```json
{
  "nodes": [
    {
      "name": "Get Yesterday's Calls",
      "type": "n8n-nodes-zadarma.zadarma", 
      "parameters": {
        "resource": "statistics",
        "operation": "getStats",
        "startDate": "{{DateTime.now().minus({days: 1}).startOf('day')}}",
        "endDate": "{{DateTime.now().minus({days: 1}).endOf('day')}}"
      }
    }
  ]
}
```

### Automated Recording Download

```json
{
  "nodes": [
    {
      "name": "Get Call Stats", 
      "type": "n8n-nodes-zadarma.zadarma",
      "parameters": {
        "resource": "statistics", 
        "operation": "getStats"
      }
    },
    {
      "name": "Filter Recorded Calls",
      "type": "n8n-nodes-base.filter",
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.is_recorded}}",
              "operation": "equal",
              "value2": "true"
            }
          ]
        }
      }
    },
    {
      "name": "Get Recording Link",
      "type": "n8n-nodes-zadarma.zadarma",
      "parameters": {
        "resource": "recording",
        "operation": "getLink", 
        "callId": "={{$json.call_id}}"
      }
    }
  ]
}
```

---

## 🔐 Authentication

This node implements Zadarma's official HMAC-SHA1 authentication:

- **Parameter Sorting**: Alphabetical ordering
- **RFC1738 Encoding**: Proper URL encoding (spaces as `+`)
- **HMAC-SHA1 Signing**: Base64 of hexadecimal digest
- **Automatic Headers**: `Authorization: api_key:signature`

The authentication algorithm has been thoroughly tested and matches the official Python implementation.

---

## 🐛 Troubleshooting

### Node Not Appearing

1. Ensure n8n is fully restarted after installation
2. Check that the package was installed in the correct directory
3. Verify n8n logs for any loading errors

### 401 Authentication Errors

1. Verify your API credentials in **Credentials** settings
2. Check that your Zadarma account has API access enabled
3. Ensure you're using the correct environment (production/sandbox)

### No Data Returned

1. Verify the date range contains call records
2. Check that calls were actually recorded (`is_recorded: true`)
3. Ensure your API key has access to the requested data

---

## 📚 API Reference

For complete API documentation, see:
- [Zadarma API Documentation](https://zadarma.com/en/support/api/)
- [Authentication Guide](https://zadarma.com/en/support/api/#auth)

---

## 🔄 Version History

### v1.0.1
- 🐛 **Fixed**: RFC1738 encoding for proper signature generation
- ✅ **Improved**: Authentication algorithm now matches Python reference
- 📝 **Updated**: Enhanced error messages and validation

### v1.0.0  
- 🎉 **Initial**: First release with basic call statistics and recording operations
- ⚡ **Features**: HMAC-SHA1 authentication, date range queries
- 🔧 **Support**: Production and sandbox environments

---

## 🤝 Contributing

Issues and pull requests are welcome at:
[https://github.com/zerox9dev/zadarma-api](https://github.com/zerox9dev/zadarma-api)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**zerox9dev**
- Email: Mirvald.vadim@icloud.com
- GitHub: [@zerox9dev](https://github.com/zerox9dev)

---

*This node is not officially affiliated with Zadarma but provides reliable integration using their public API.*