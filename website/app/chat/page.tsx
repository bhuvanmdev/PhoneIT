"use client";
import Chat from "@/components/Chat";
import ResponseChat from "@/components/ResponseChat";
import { SendIcon } from "lucide-react";
import { useState } from "react";

const page = () => {
  const [messageData, setMessageData] = useState<any>([]);
  const [inputMsg, setInputMsg] = useState("");
  const handleEnter = () => {
    setMessageData((prevData: any) => [
      ...prevData,
        { message: inputMsg, sender: "user" },
    ]);
    setInputMsg("");
  }
  return (
    <div className="flex min-h-screen justify-between p-24">
      <div className="flex w-1/2 flex-col">
        <div className="text-2xl">Previous conversations</div>
      </div>
      <div className="flex flex-col w-1/2 relative">
        <div className="ml-4 h-full border-2 rounded-md relative">
          <div className="p-4 text-xl absolute w-full">ChatBot</div>
          <div className="p-4 pr-0 justify-end flex flex-col my-12 h-xlg">
            <div className="overflow-auto pr-2">
              {messageData.length > 0 ? (
                messageData.map((e: any) =>
                  e.sender !=='user' ? <Chat msg={e.message} /> : <ResponseChat msg={e.message} />
                )
              ) : (
                <div className="text-center text-slate-500">
                  Start chatting here!!
                </div>
              )}
            </div>
          </div>
          <div className="absolute bottom-0 w-full">
            <div className="relative">
            <input
              type="text"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleEnter()
                }
              }}
                value={inputMsg}
                onChange={(e) => setInputMsg(e.target.value)}
              className="w-full p-4 border-t-2 border-gray-300 text-slate-950"
              placeholder="Type your message here"
            />
            <button className="absolute right-2 top-1 z-50 bg-slate-900 rounded-xl p-4" onClick={handleEnter}><SendIcon size={16}/></button>
            
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default page;
