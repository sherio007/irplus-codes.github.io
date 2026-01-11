# Samsung TV Control System

A complete system for controlling Samsung TVs using WebSocket communication with your TV token.

## Files Included

- `send_key_direct.js` - Direct key sending via WebSocket
- `force_open_browser.js` - Force the TV to open a specific webpage
- `rccli_bridge.py` - Python-based HTTP-to-WebSocket bridge with web interface
- `package.json` - Node.js dependencies and scripts

## Prerequisites

- Samsung TV connected to the same network
- TV token (already configured: `78091086`)
- TV IP address: `192.168.23.25`
- Laptop IP address: `192.168.23.20`

## Installation

1. Install Node.js dependencies:
```bash
npm install
```

2. Install Python dependencies:
```bash
pip install websockets
```

## Usage Options

### Option 1: Direct Key Sending
```bash
node send_key_direct.js KEY_MENU
```
Available keys: `KEY_HOME`, `KEY_UP`, `KEY_DOWN`, `KEY_LEFT`, `KEY_RIGHT`, `KEY_ENTER`, `KEY_VOLUP`, `KEY_VOLDOWN`, `KEY_CHUP`, `KEY_CHDOWN`, etc.

### Option 2: Force Browser to Open
```bash
node force_open_browser.js
```
This will open the TV browser to `http://192.168.23.20:8080/control.html`

### Option 3: Web-Based Control (Recommended)
1. Start the Python bridge server:
```bash
python rccli_bridge.py
```

2. On your TV, navigate to: `http://192.168.23.20:8080/control.html`
   OR access from your laptop: `http://localhost:8080/control.html`

3. Use the web-based remote control interface

### NPM Scripts
- `npm start` - Run the direct key sender
- `npm run browser` - Force open the browser on TV
- `npm run bridge` - Start the web bridge server

## Features

- ✅ Direct WebSocket communication with TV
- ✅ No external executables needed
- ✅ Complete web-based remote control
- ✅ Supports all standard Samsung TV keys
- ✅ Built-in browser launcher
- ✅ Channel changing functionality
- ✅ Volume and navigation controls

## Troubleshooting

- Make sure your TV is powered on and connected to the network
- Verify the TV token is still valid (may need regeneration after some time)
- Check that firewall settings allow connections on port 8002 (TV) and 8080 (laptop)
- If connection fails, try restarting the TV or regenerating the token

## Security Note

⚠️ This implementation disables SSL certificate verification for compatibility with Samsung TV certificates. Only use on trusted networks.
