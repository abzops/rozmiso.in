const WebSocket = require('ws');
const fs = require('fs');

const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
const port = content[0];
const wsPath = content[1];
const wsUrl = `ws://127.0.0.1:${port}${wsPath}`;

console.log('Testing raw WS to:', wsUrl);

const ws = new WebSocket(wsUrl, {
  headers: {
    'Host': `127.0.0.1:${port}`,
    'Origin': 'http://127.0.0.1:9222'
  },
  handshakeTimeout: 3000
});

ws.on('open', () => {
  console.log('WS OPENED!');
  ws.send(JSON.stringify({ id: 1, method: 'Target.getTargets' }));
});

ws.on('message', data => {
  console.log('WS MESSAGE:', data.toString().substring(0, 300));
  ws.close();
});

ws.on('error', err => {
  console.log('WS ERROR:', err.message);
});

setTimeout(() => {
  console.log('Timeout reached. Exiting.');
  process.exit(0);
}, 4000);
