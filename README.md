# 🎵 Zadarma Audio Downloader

**Automated call recording downloads from Zadarma telephony platform**

This repository provides **two complete solutions** for downloading call audio recordings from the Zadarma API:

1. **🐍 Python Implementation** - Standalone script for automated downloads
2. **🔗 n8n Custom Node** - Professional workflow automation integration

---

## 🌟 Features

- ✅ **Automated Authentication** - Secure HMAC-SHA1 signature generation
- ✅ **Call Statistics Retrieval** - Get call records from specified date ranges  
- ✅ **Audio Download Links** - Generate download URLs for recorded calls
- ✅ **Flexible Time Ranges** - Configure from hours to months of history
- ✅ **Production Ready** - Robust error handling and retry logic
- ✅ **Multiple Deployment Options** - Python scripts or n8n workflows

---

## 🚀 Quick Start

### Option 1: Python Implementation

``bash
# Clone repository
git clone https://github.com/zerox9dev/zadarma-api.git
cd zadarma-api

# Install dependencies  
pip install -r requirements.txt

# Configure credentials
cp .env.example .env
# Edit .env with your API credentials

# Run downloader
python3 run.py
```

### Option 2: n8n Custom Node

```bash
# Install the custom node
npm install n8n-nodes-zadarma

# Restart n8n
# The "Zadarma" node will appear in your node palette
```

---

## 📁 Repository Structure

```
zadarma-api/
├── 🐍 Python Implementation
│   ├── run.py                 # Entry point
│   ├── requirements.txt       # Dependencies  
│   ├── config/settings.py     # Configuration loader
│   └── src/
│       ├── downloader.py      # Download orchestrator
│       └── zadarma/api.py     # API client with authentication
│
├── 🔗 n8n Custom Node  
│   ├── package.json           # NPM package configuration
│   ├── credentials/           # Zadarma API credentials definition
│   └── nodes/Zadarma/         # Main node implementation
│
└── 📄 Documentation
    ├── README.md              # This file
    └── .env.example           # Environment template
```

---

## 🐍 Python Implementation

### Prerequisites

- Python 3.7+
- `pip` package manager
- Zadarma API credentials

### Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```env
   API_KEY=your_zadarma_api_key
   API_SECRET=your_zadarma_api_secret
   SANDBOX=false
   DAYS_BACK=1
   ```

3. **Run the Downloader**
   ```bash
   python3 run.py
   ```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Your Zadarma API key | Required |
| `API_SECRET` | Your Zadarma API secret | Required |  
| `SANDBOX` | Use sandbox environment | `false` |
| `DAYS_BACK` | Days of history to fetch | `1` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

### Python API Usage

```python
from src.zadarma.api import ZadarmaAPI

# Initialize client
client = ZadarmaAPI(
    key="your_api_key",
    secret="your_api_secret", 
    sandbox=False
)

# Get call statistics
stats = client.call('/v1/statistics/pbx/', {
    'start': '2024-01-01 00:00:00',
    'end': '2024-01-02 00:00:00'
})

# Request recording download
recording = client.call('/v1/pbx/record/request/', {
    'call_id': 'your_call_id'
})
```

---

## 🔗 n8n Custom Node

### Installation

#### Method 1: NPM (Recommended)

```bash
npm install n8n-nodes-zadarma
```

#### Method 2: Manual Installation

```bash
# Navigate to n8n user directory
cd ~/.n8n/nodes

# Install the package
npm install n8n-nodes-zadarma

# Restart n8n
```

### Node Configuration

1. **Add Credentials**
   - Go to **Credentials** → **Create New**
   - Select **Zadarma API** 
   - Enter your API Key and Secret

2. **Add Zadarma Node**
   - Drag **Zadarma** node from the palette
   - Select your credentials
   - Configure the operation:
     - **Resource**: Call Statistics / Call Recording
     - **Operation**: Get Call Statistics / Get Download Link

### Available Operations

#### 📊 Call Statistics
- **Purpose**: Retrieve call records for a date range
- **Parameters**: 
  - Start Date/Time
  - End Date/Time
- **Returns**: Array of call records with metadata

#### 🎵 Call Recording  
- **Purpose**: Get download link for specific call recording
- **Parameters**:
  - Call ID
- **Returns**: Download URL and recording metadata

### n8n Workflow Example

```json
{
  "nodes": [
    {
      "name": "Get Call Stats",
      "type": "n8n-nodes-zadarma.zadarma",
      "parameters": {
        "resource": "statistics",
        "operation": "getStats", 
        "startDate": "2024-01-01T00:00:00.000Z",
        "endDate": "2024-01-02T00:00:00.000Z"
      }
    }
  ]
}
```

---

## 🔐 Authentication

Both implementations use **HMAC-SHA1 signature authentication** following Zadarma's official specification:

### Algorithm Overview

1. **Parameter Sorting** - Sort all request parameters alphabetically
2. **Query String Building** - Create RFC1738-encoded parameter string  
3. **MD5 Hashing** - Generate MD5 hash of parameter string
4. **String Construction** - Combine: `method + params + md5_hash`
5. **HMAC Signing** - Create HMAC-SHA1 signature with API secret
6. **Base64 Encoding** - Encode the hexadecimal digest as Base64

### Critical Implementation Details

- **Encoding Standard**: RFC1738 (spaces as `+`, not `%20`)
- **HMAC Format**: Base64 of hexadecimal digest string, **not** raw bytes
- **Parameter Inclusion**: All parameters including `format=json` must be signed

---

## 📋 API Reference

### Zadarma Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/statistics/pbx/` | GET | Retrieve call statistics |
| `/v1/pbx/record/request/` | GET | Request call recording download |

### Response Format

```json
{
  "status": "success",
  "start": "2024-01-01 00:00:00", 
  "end": "2024-01-02 00:00:00",
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

---

## 🛠️ Development

### Building the n8n Node

```bash
cd n8n-nodes-zadarma
npm run build
```

### Testing

Both implementations include comprehensive test coverage:

- **Python**: Unit tests with pytest
- **n8n Node**: Local execution tests with real API calls

### Publishing Updates

```bash
# Update version in package.json
npm version patch

# Publish to npm  
npm publish
```

---

## 🐛 Troubleshooting

### Common Issues

#### 401 Unauthorized Error
- **Cause**: Incorrect signature generation or expired credentials
- **Solution**: Verify API credentials and signature algorithm implementation

#### Missing Call Recordings  
- **Cause**: Calls not recorded or outside time range
- **Solution**: Check `is_recorded` field and adjust date parameters

#### Timeout Errors
- **Cause**: Network issues or large result sets
- **Solution**: Reduce time range or increase timeout values

### Debug Mode

Enable detailed logging:

```bash
# Python
LOG_LEVEL=DEBUG python3 run.py

# n8n  
# Check n8n logs for node execution details
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/zerox9dev/zadarma-api/issues)
- **Documentation**: [Zadarma API Docs](https://zadarma.com/en/support/api/)
- **Email**: Mirvald.vadim@icloud.com

---

## 🏆 Achievements

- ✅ **Stable Authentication** - Resolves common 401 signature issues
- ✅ **Production Tested** - Used in real telephony workflows
- ✅ **Multi-Platform** - Python scripts + n8n workflows
- ✅ **NPM Published** - Available as `n8n-nodes-zadarma`

---

*Built with ❤️ for seamless Zadarma API integration*

# Zadarma API Integration

**Two solutions for automated Zadarma call recording downloads:**

- **🐍 Python Script** - Standalone automation
- **🔗 n8n Custom Node** - Workflow integration

## Quick Start

### Python Implementation
``bash
git clone https://github.com/zerox9dev/zadarma-api.git
cd zadarma-api
pip install -r requirements.txt
cp .env.example .env  # Add your API credentials
python3 run.py
```

### n8n Custom Node
```bash
npm install n8n-nodes-zadarma
# Restart n8n, add Zadarma credentials, use the node
```

## Features

- ✅ HMAC-SHA1 authentication (RFC1738 compliant)
- ✅ Call statistics retrieval
- ✅ Recording download links
- ✅ Production tested

## Configuration

Edit `.env` file:
```env
API_KEY=your_zadarma_api_key
API_SECRET=your_zadarma_api_secret
SANDBOX=false
DAYS_BACK=1
```

## Python Usage

```python
from src.zadarma.api import ZadarmaAPI

client = ZadarmaAPI(key="api_key", secret="api_secret")
stats = client.call('/v1/statistics/pbx/', {
    'start': '2024-01-01 00:00:00',
    'end': '2024-01-02 00:00:00'
})
```

## n8n Node Operations

- **Call Statistics**: Get call records for date range
- **Recording Download**: Get download link for call ID

## Repository Structure

```
├── app/                    # Python implementation
├── n8n-nodes-zadarma/     # NPM package
├── run.py                 # Python entry point
└── requirements.txt       # Python dependencies
```

## Links

- **NPM**: `n8n-nodes-zadarma@1.0.1`
- **GitHub**: https://github.com/zerox9dev/zadarma-api
- **Zadarma API Docs**: https://zadarma.com/en/support/api/
