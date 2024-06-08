import { NextResponse } from "next/server";

// app/api/call/route.ts


let isCallOngoing: boolean = false;
let isCallEnded: boolean = false;
let isChatMessage: boolean = false;
let messageValue: string = "Waiting for Call";
let chatMessageValue: string | null = null;
let isAIResponse: boolean = false;
export async function GET(request: Request) {
    console.log("API Call made to check call status")
    const currMsg=chatMessageValue;
    const currIsMsg=isChatMessage;
    let currAI=isAIResponse;
    chatMessageValue=null;
    isChatMessage=false;
    return NextResponse.json({ 
        isCallOngoing: isCallOngoing , 
        isCallEnded : isCallEnded,
        chatMessage : currMsg,
        isChatMessage : currIsMsg,
        isAIResponse: currAI
    }, { status: 200 }, 
        );
}

export async function POST(request: Request) {
    const origin = request.headers.get('origin');
    const body = await request.json();
    isCallOngoing = body.isCallOngoing;
    isCallEnded = body.isCallEnded;
    isChatMessage = body.isChatMessage;
    isAIResponse = body.isAIResponse;
    if (body.isChatMessage != null){
    chatMessageValue = body.chatMessage;
    }
    return NextResponse.json({ message: 'Received at website server' }, { status: 200 });
}
