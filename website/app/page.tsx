'use client'
import { useState, useEffect } from 'react';

export default function Home() {
  const [callStatus, setCallStatus] = useState('Waiting for call');

  useEffect(() => {
    const fetchCallStatus = async () => {
      try {
        const response = await fetch('/api/call');
        console.log("API Call made to check call status")
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log("API Call response", data)
        console.log("Is Message" , data.isChatMessage)
        console.log("Message is" , data.chatMessage)
        if (data.isCallEnded) { 
          setCallStatus('Call Ended');
          return;
        }
        setCallStatus(
          data.isCallOngoing ? 'Call Ongoing' : 'Waiting for call');
      } catch (error) {
        console.error('Error fetching call status:', error);
      }
    };

    const intervalId = setInterval(fetchCallStatus, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      {callStatus}
      <button onClick={() => setCallStatus('Call Ongoing')}>Receive Call</button>
    </main>
  );
}
