import { createServer } from 'http';
import { parse, UrlWithStringQuery, UrlWithParsedQuery } from 'url';
import next from 'next';
import  WebSocket  from 'ws';

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

let wss: WebSocket.Server;

app.prepare().then(() => {
  const server = createServer((req, res) => {
    const parsedUrl: UrlWithStringQuery | UrlWithParsedQuery = parse(req.url || '', true);
    handle(req, res, parsedUrl);
  });

  wss = new WebSocket.Server({ server });

  wss.on('connection', () => {
    console.log('Client connected');
  });

  server.listen(3000, () => {
    console.log('> Ready on http://localhost:3000');
  });
});

export { wss };
