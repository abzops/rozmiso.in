const http = require('http');
const fs = require('fs');
const path = require('path');

// Read DevToolsActivePort
const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
const port = parseInt(content[0], 10);
const wsPath = content[1];

console.log(`DevTools port: ${port}, path: ${wsPath}`);

// Let's test sending a basic CDP command over WebSocket
// Or test puppeteer-core
const crypto = require('crypto');
const key = crypto.randomBytes(16).toString('base64');

const req = http.request({
  host: '127.0.0.1',
  port: port,
  path: wsPath,
  headers: {
    'Connection': 'Upgrade',
    'Upgrade': 'websocket',
    'Sec-WebSocket-Version': '13',
    'Sec-WebSocket-Key': key
  }
});

req.on('upgrade', (res, socket, head) => {
  console.log('WebSocket upgrade successful! Connected to Chrome DevTools CDP!');
  
  // Format a simple CDP message: Target.getTargets
  const msg = JSON.stringify({ id: 1, method: 'Target.getTargets' });
  const msgBuf = Buffer.from(msg);
  
  // Create unmasked/masked WS frame
  // Client to server frames must be masked
  const mask = crypto.randomBytes(4);
  const frame = Buffer.alloc(2 + 4 + msgBuf.length);
  frame[0] = 0x81; // FIN + text opcode
  frame[1] = 0x80 | msgBuf.length; // Mask bit + length (< 126)
  mask.copy(frame, 2);
  for (let i = 0; i < msgBuf.length; i++) {
    frame[6 + i] = msgBuf[i] ^ mask[i % 4];
  }
  
  socket.write(frame);
  
  socket.on('data', chunk => {
    console.log('Received raw frame of length:', chunk.length);
    // Parse WS frame
    let payload = chunk;
    if (chunk[0] === 0x81) {
      let len = chunk[1] & 0x7f;
      let offset = 2;
      if (len === 126) {
        len = chunk.readUInt16BE(2);
        offset = 4;
      } else if (len === 127) {
        offset = 10;
      }
      const dataStr = chunk.slice(offset).toString('utf8');
      try {
        const parsed = JSON.parse(dataStr);
        console.log('CDP targets found:');
        if (parsed.result && parsed.result.targetInfos) {
          parsed.result.targetInfos.forEach(t => {
            console.log(` - [${t.type}] ${t.title} (${t.url})`);
          });
        }
      } catch (e) {
        console.log('Data string:', dataStr);
      }
    }
    socket.end();
  });
});

req.on('error', err => {
  console.error('Request error:', err);
});

req.end();
