import { NextResponse } from "next/server";

// app/api/call/route.ts


let isCallOngoing: boolean = false;
let isCallEnded: boolean = false;
let messageValue: string = "Waiting for Call";
let chatMessageValue: string | null = null;

export async function GET(request: Request) {
    console.log("API Call made to check call status")
    return NextResponse.json({ isCallOngoing: isCallOngoing , 
        message : messageValue ,
        isCallEnded : isCallEnded,
        chatMessage : chatMessageValue
    }, { status: 200 }, 
        );
}

export async function POST(request: Request) {
    const origin = request.headers.get('origin');
    const body = await request.json();
    isCallOngoing = body.isCallOngoing;
    isCallEnded = body.isCallEnded;
    if (body.isChatMessage != null){
    chatMessageValue = body.chatMessage;
    }
    return NextResponse.json({ message: 'Received at website server' }, { status: 200 });
}
