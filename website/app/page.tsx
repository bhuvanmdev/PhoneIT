"use client";
import Chat from "@/components/Chat";
import ResponseChat from "@/components/ResponseChat";
import { useState, useEffect } from "react";

export default function Home() {
  const [callStatus, setCallStatus] = useState("Waiting for call");
  const [messageData, setMessageData] = useState<any>([
    
  ]);
  useEffect(() => {
    const fetchCallStatus = async () => {
      try {
        const response = await fetch("/api/call");
        console.log("API Call made to check call status");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("API Call response", data);
        console.log("Is Message", data.isChatMessage);
        console.log("Message is", data.chatMessage);
        if (data.isChatMessage)
          setMessageData((prevData:any) => [...prevData, data.chatMessage]);
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
        <div className="text-4xl text-center h-full w-full flex flex-col items-center justify-center">
          {callStatus}
        </div>
      </div>
      <div className="flex flex-col w-1/2 relative">
        <div className="ml-4 h-full border-2 rounded-md">
          <div className="p-4 text-xl absolute w-full">Live transcription</div>
          <div className="p-4 pr-0 justify-end flex flex-col mt-12 h-xxlg">
            <div className="overflow-auto pr-2">
              {messageData.length>0?messageData.map((e:string, i:number) =>
                i % 2 == 0 ? <Chat msg={e} /> : <ResponseChat msg={e} />
              ):<div className="text-center text-slate-500">Start a phone call to start receiving messages</div>}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
