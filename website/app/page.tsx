"use client";
import Chat from "@/components/Chat";
import ResponseChat from "@/components/ResponseChat";
import { useState, useEffect } from "react";
import { ArrowLeftCircle, ArrowRight, Mic } from "lucide-react";
import { collection, doc, getDocs, setDoc } from "firebase/firestore";
import { db } from "./firebase";
import { toast } from "react-toastify";

import "react-toastify/dist/ReactToastify.css";

export default function Home() {
  const [callStatus, setCallStatus] = useState("Waiting for call");
  const [isAIResponse, setIsAIResponse] = useState(false);
  const [messageData, setMessageData] = useState<any>([]);
  const [prevCallsData, setPrevCallsData] = useState<any>([]);

  const [currHistory, setCurrHistory] = useState<any>([]);
  useEffect(() => {
    if (callStatus === "Call Ended") {
      return;
    }

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
        setIsAIResponse(data.isAIResponse);
        if (data.isChatMessage) {
          setMessageData((prevData: any) => [...prevData, data.chatMessage]);
        }
        if (data.isCallEnded) {
          setCallStatus("Call Ended");
          return;
        }
        setCallStatus(data.isCallOngoing ? "Call Ongoing" : "Waiting for call");
      } catch (error) {
        console.error("Error fetching call status:", error);
      }
    };

    const intervalId = setInterval(fetchCallStatus, 2000);

    return () => clearInterval(intervalId);
  }, [callStatus]);

  const parseAIResponse = (response: string) => {
    return response.replace(/<say>|<\/say>/g, "");
  };
  const getCallsData = async () => {
    try {
      const callsRef = collection(db, "calls");
      const callsSnapshot = await getDocs(callsRef);
      const callsData = callsSnapshot.docs.map((doc) => {
        return { data: doc.data(), docId: doc.id };
      });
      setPrevCallsData(callsData);
      console.log(callsData);
    } catch (error) {
      console.error("Error fetching calls data:", error);
    }
  };

  useEffect(() => {
    getCallsData();
  }, []);
  const clearHistory = () => {
    setCurrHistory([]);
  };
  return (
    <main className="flex min-h-screen justify-between p-24">
      {currHistory.data && (
        <div className="absolute h-screen w-screen top-0 bottom-0 left-0 right-0 bg-black z-40 mt-16 p-12 overflow-x-hidden">
          <div className="flex text-xl justify-between mb-4">
            <div className="flex gap-4">
              <div onClick={clearHistory}>
                <ArrowLeftCircle />
              </div>
              Transcription History
            </div>
            <div>{currHistory.data.callStatus}</div>
          </div>
          <div>
            {currHistory.data.messages.map((data: any, index: number) => {
              return index % 2 == 0 ? (
                <Chat key={index} msg={data} />
              ) : (
                <ResponseChat key={index} msg={data} />
              );
            })}
          </div>
        </div>
      )}
      <div className="flex w-1/2 flex-col justify-between">
        <div
          className="height-50 text-4xl h-1/2 text-center flex flex-col items-center justify-center gap-4"
          onClick={async () => {
            setCallStatus("Call Ended");
            const dateAndTimeNow = new Date().toLocaleString();
            //replace the / with - in the date
            const dateAndTimeNowFormatted = dateAndTimeNow.replace(/\//g, "-");

            try {
              await setDoc(doc(db, "calls", dateAndTimeNowFormatted), {
                callStatus: "Call Ended",
                callTime: dateAndTimeNowFormatted,
                messages: messageData,
              });
              toast.success("Call Ended Successfully!");
            } catch (e) {
              console.error("Error writing document: ", e);
              toast.error("Error writing document");
            }
          }}
        >
          {callStatus === "Call Ongoing" ? (
            <div className="p-4 glow-icon rounded-full">
              <Mic className="" size={64} />
            </div>
          ) : null}
          {callStatus}
        </div>
        <div className="height-50 overflow-auto">
          <div className="mb-2 text-xl">Previous calls</div>
          <div className="">
            <div className="flex flex-col gap-4">
              {prevCallsData.map((data: any, index: number) => {
                return (
                  <div
                    key={index}
                    onClick={() => {
                      setCurrHistory(data);
                      console.log(data);
                    }}
                    className="flex justify-between items-center border-2 border-slate-800 rounded-md p-4"
                  >
                    <div className="">{data.docId}</div>
                    <ArrowRight size={16} className=" cursor-pointer" />
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
      <div className="flex flex-col w-1/2 relative">
        <div className="ml-4 h-full border-2 rounded-md">
          <div className="p-4 text-xl absolute w-full">Live transcription</div>
          <div className="p-4 pr-0 justify-end flex flex-col mt-12 h-xxlg">
            <div className="overflow-auto pr-2">
              {messageData.length > 0 ? (
                messageData.map((e: string, i: number) =>
                  i % 2 !== 0 ? (
                    <Chat msg={parseAIResponse(e)} />
                  ) : (
                    <ResponseChat msg={e} />
                  )
                )
              ) : (
                <div className="text-center text-slate-500">
                  Start a phone call to start receiving messages
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
