'use client';
import { useState, useEffect } from 'react';

export default function Home() {
  const [callStatus, setCallStatus] = useState('Waiting for call');

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:3000');

    socket.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      setCallStatus(data.message);
    });

    return () => {
      socket.close();
    };
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      {callStatus}
      <button onClick={() => setCallStatus('Call Ongoing')}>Receive Call</button>
    </main>
  );
}
