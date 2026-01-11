// ============================================
// FILE 2: force_open_browser.js
// Force TV to open browser with control page
// ============================================

const WebSocket = require('ws');

const TV_IP = '192.168.23.25';
const MY_TOKEN = '78091086'; 
const LAPTOP_IP = '192.168.23.20';
const NAME = Buffer.from('Master_Controller').toString('base64'); 

console.log('');
console.log('=' .repeat(60));
console.log('  🌐 Force Opening Browser on TV');
console.log('=' .repeat(60));
console.log(`TV: ${TV_IP}`);
console.log(`Target: http://${LAPTOP_IP}:8080/control.html`);
console.log('=' .repeat(60));
console.log('');

const wsUrl = `wss://${TV_IP}:8002/api/v2/channels/samsung.remote.control?name=${NAME}&token=${MY_TOKEN}`;

const ws = new WebSocket(wsUrl, { 
    rejectUnauthorized: false,
    handshakeTimeout: 5000
});

ws.on('open', () => {
    console.log('✅ Connected to TV!');
    console.log('🚀 Forcing Browser to Open...');
    console.log('');
    
    const launchCommand = {
        method: 'ms.channel.emit',
        params: {
            event: 'ed.apps.launch',
            to: 'host',
            data: {
                appId: 'org.tizen.browser',
                action_type: 'NATIVE_LAUNCH',
                metaTag: `http://${LAPTOP_IP}:8080/control.html`
            }
        }
    };
    
    ws.send(JSON.stringify(launchCommand));
    
    setTimeout(() => { 
        console.log('✅ Browser launch command sent!');
        console.log('');
        console.log('📺 Browser should open on TV now');
        console.log(`🌐 URL: http://${LAPTOP_IP}:8080/control.html`);
        console.log('');
        ws.close(); 
        process.exit(0); 
    }, 2000);
});

ws.on('error', (err) => {
    console.error('❌ Connection error:', err.message);
    console.log('');
    console.log('💡 Possible solutions:');
    console.log('  - Check TV is ON');
    console.log('  - Check token is correct: 78091086');
    console.log('  - Try regenerating token');
    process.exit(1);
});

ws.on('message', (data) => {
    try {
        const msg = JSON.parse(data.toString());
        console.log('📩 TV Response:', msg);
    } catch (e) {
        console.log('📩 Raw message:', data.toString());
    }
});