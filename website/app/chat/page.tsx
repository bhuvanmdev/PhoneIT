'use client'
import Chat from "@/components/Chat"
import ResponseChat from "@/components/ResponseChat"
import { useState } from "react"

const page = () => {
    const [messageData,setMessageData] = useState<any>([])
  return (
    <div className="flex min-h-screen justify-between p-24">
        <div className="flex w-1/2 flex-col">
        <div className="text-2xl">
            Previous conversations
        </div>
        </div>
        <div className="flex flex-col w-1/2 relative">
        <div className="ml-4 h-full border-2 rounded-md">
          <div className="p-4 text-xl absolute w-full">ChatBot</div>
          <div className="p-4 pr-0 justify-end flex flex-col mt-12 h-xxlg">
            <div className="overflow-auto pr-2">
              {messageData.length>0?messageData.map((e:any, i:number) =>
                i%2==0 ? <Chat msg={e} /> : <ResponseChat msg={e} />
              ):<div className="text-center text-slate-500">Start chatting here!!</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default page