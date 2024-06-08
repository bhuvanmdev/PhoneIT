"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [callStatus, setCallStatus] = useState("Waiting for call");

  useEffect(() => {
    const fetchCallStatus = async () => {
      try {
        const response = await fetch("/api/call");
        console.log("API Call made to check call status");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("API Call response", data.flag);
        if (data.isCallEnded) {
          setCallStatus("Call Ended");
          return;
        }
        setCallStatus(data.isCallOngoing ? "Call Ongoing" : "Waiting for call");
      } catch (error) {
        console.error("Error fetching call status:", error);
      }
    };

    const intervalId = setInterval(fetchCallStatus, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <main className="flex min-h-screen justify-between p-24">
      <div className="flex w-1/2 flex-col justify-between">
        <div className="text-4xl text-center h-full w-full flex flex-col items-center justify-center">{callStatus}</div>
        <button onClick={() => setCallStatus("Call Ongoing")}>
          Receive Call
        </button>
      </div>
      <div className="h-full w-1/2">
        <div className="m-4 p-4 border-2">
          <div>Live transcription</div>
          <div>
            <div>Messages</div>
            <div>
              <input type="text" />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
