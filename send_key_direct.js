// ============================================
// FILE 1: send_key_direct.js
// Direct key sender using WebSocket + Token
// ============================================

const WebSocket = require('ws');

const TV_IP = '192.168.23.25';
const MY_TOKEN = '78091086'; 
const NAME = Buffer.from('Master_Controller').toString('base64');

function sendKey(key) {
    const wsUrl = `wss://${TV_IP}:8002/api/v2/channels/samsung.remote.control?name=${NAME}&token=${MY_TOKEN}`;
    
    const ws = new WebSocket(wsUrl, { 
        rejectUnauthorized: false,
        handshakeTimeout: 5000
    });

    ws.on('open', () => {
        console.log(`✅ Sending Key: ${key}`);
        
        const payload = {
            method: 'ms.channel.emit',
            params: {
                event: 'ed.remote.control',
                to: 'host',
                data: { 
                    type: 'method', 
                    key: key, 
                    base64: 'false' 
                }
            }
        };
        
        ws.send(JSON.stringify(payload));
        
        setTimeout(() => { 
            ws.close(); 
            process.exit(0); 
        }, 500);
    });

    ws.on('error', (err) => { 
        console.error(`❌ Error: ${err.message}`);
        process.exit(1); 
    });
    
    ws.on('close', () => {
        console.log('🔌 Connection closed');
    });
}

const key = process.argv[2] || 'KEY_HOME';
sendKey(key);