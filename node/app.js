const { StreamrClient } = require('streamr-client');
const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

async function subscribeTest() {
    // not sensitive
    const privateKey = 'a8b2f15fa298f086e3fd80990bf0380184f90a7c9dce738dd3e3418e2892ff54'
    const streamr = new StreamrClient({
        auth: {
            privateKey: privateKey,
        },
    })
    const streamId = 'binance-streamr.eth/ETHUSDT/ticker'
    //const streamId = 'streamr.eth/demos/twitter/sample'
    const subscription = await streamr.subscribe({
        stream: streamId,
    },
    (message) => {
        // This function will be called when new messages occur
        console.log(JSON.stringify(message))
    })
}
subscribeTest();