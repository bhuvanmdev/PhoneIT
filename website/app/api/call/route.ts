// app/api/call/route.ts

import { NextResponse } from "next/server";
import { wss }   from '../../server'; // Import the WebSocket server
// import * as wss from "../../server"
export async function POST(request: Request) {
  const origin = request.headers.get('origin');

  if (origin !== 'http://localhost:3000') {
    return NextResponse.json({ message: 'Forbidden' }, { status: 403 });
  }

  // Send a WebSocket message to all connected clients
  wss.clients.forEach((client: any)  => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({ message: 'Call Ongoing' }));
    }
  });

  return NextResponse.json({ message: 'Call Ongoing' }, { status: 200 });
}
