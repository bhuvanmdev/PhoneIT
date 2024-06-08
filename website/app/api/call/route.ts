import { NextResponse } from "next/server";

// app/api/call/route.ts


let flagValue: boolean = false;

export async function GET(request: Request) {
    return NextResponse.json({ flag: flagValue }, { status: 200 });
}

export async function POST(request: Request) {
    const origin = request.headers.get('origin');
    const body = await request.json();
    flagValue = body.flag;

    return NextResponse.json({ message: 'Call Ongoing' }, { status: 200 });
}
