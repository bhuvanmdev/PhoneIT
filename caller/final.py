from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from os.path import join
import google.generativeai as genai
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import requests
import re

dotenv_path = join("./.env")
load_dotenv(dotenv_path)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
URL = os.getenv("URL")
TO_NUM = os.getenv("TO_NUM")
GKEY = os.getenv("GKEY")
LLM = os.getenv("LLM")
PROMPT = f"""You are a helpful AI voice all agent who responds to user queries. Please generate text output that is optimized for Text-to-Speech (TTS) models. Follow these guidelines to ensure clarity and ease of understanding:
1. Use Proper Grammar and Punctuation: Ensure that the text is grammatically correct and punctuated appropriately.
2. Avoid Emojis and Problamatic Special Characters: Do not include emojis, symbols, or any special characters that are not necessary for the content. This includes boldizing, intalics, and other formatting (i.e no "**", ":" to be included).
3. Use Full Words and Sentences: Do not use abbreviations, acronyms, or contractions unless they are widely recognized and necessary.
4. Maintain a Formal and Friendly Tone: Keep the tone formal and professional.
5. Avoid Slang and Colloquialisms: Use standard language and avoid regional slang or colloquial expressions.
6. Structure the Text Clearly: Use paragraphs to separate different ideas and ensure the text flows logically.
7. Use Simple Language: Avoid complex words or phrases when simpler alternatives are available.
8. Provide Clear Context: Ensure that the content is self-explanatory and does not rely on external context to be understood.
9. Make The Text Concise: Keep the text concise and to the point, avoiding unnecessary details or information.
10. Use SSML format: Format the text into "twilio's" version of SSML between <say> and </say> tag. There can be only 1 <say> and </say> tag.
Example:
User: I have lost my wallet, how do i get it back?
AI: "<Say>To make a phone call, you will need a phone and the person's phone number. First, locate the phone number you wish to call. Then, open your phone's dialing app.  Enter the phone number using the keypad and press the call button. The person you are calling will receive your call.</Say>"
"""
PATTERN = r"\<say\>(.*?)\</say\>"

genai.configure(api_key=GKEY)

model = genai.GenerativeModel(LLM)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
print("env values:", TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER, URL, TO_NUM, GKEY)
uuid = ''
l = []
k = 1
lang = "en-IN"
dic = {'1': 'en-IN', '2': 'hi-IN', '3': 'kn-IN', '4': 'bn-IN'}  # 0 style for kan and beng
call = s = None
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def call():
    global uuid, call
    l.clear()
    call = s = None
    k = 1
    uuid = ''
    call = client.calls.create(
        to=TO_NUM,
        from_=TWILIO_NUMBER,
        # machine_detection='Enable',
        # machine_detection_timeout=10,
        url=f'{URL}/twiml',
        method='POST', 
    )
    uuid = call.sid
    call = client.calls(uuid)
    print("Before payload")
    # Make a POST request to the specified URL
    payload = {
        'isCallOngoing': True,
        'isCallEnded': False,
        'isChatMessage': False
    }
    # headers = {
    #     "ngrok-skip-browser-warning": "69420"
    # }
    # url = 'https://a359-103-174-71-194.ngrok-free.app/api/call'
    url = "http://localhost:4000/api/call"
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Request sent to website about call initiation")
            return "Call initiated"
        else:
            print(f"Failed to initiate call: {response.status_code} - {response.text}")
            return "Failed to initiate call", response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Failed to initiate call due to request error", 500


@app.route('/twiml', methods=['POST'])
def twiml():
    global k, lang
    print("Error occurred after /twiml")
    response = VoiceResponse()
    gather = Gather(num_digits=1, action=f'{URL}/webhooks/input')
    gather.say('Press 1 for English, 2 for Hindi, 3 for Kannada, 4 for Bengali.')
    response.append(gather)
    return str(response)

@app.route('/webhooks/input', methods=['POST'])
def handle_input():
    print("Error occurred after handle input")
    global k, lang, s
    digits = request.values.get('Digits', None)
    if k == 1:
        l.append({1: 'Hello', 2: 'नमस्ते', 3: 'ನಮಸ್ಕಾರ', 4: 'হ্যালো'}.get(int(digits), 'Hello'))
        lang = dic.get(digits, 'en-IN')
    response = VoiceResponse()
    if digits == '0':
        response.say('Goodbye')
    else:
        print(f"DONE {k}")
        gather = Gather(input="speech", language=lang, action=f'{URL}/webhooks/recordings', speech_timeout=3)
        gather.say(l[-1], language=lang)
        response.append(gather)
        s = datetime.now()
    k += 1
    print(response.__str__(), response.__dir__())
    return str(response)

@app.route('/webhooks/recordings', methods=['POST'])
def handle_recordings():
    print("Error occurred after this")
    print(request, request.values)
    
    transcription = request.values.get('SpeechResult')
    print(f"\n\nTranscription: {transcription}\n\n")
    
    # url = 'https://a359-103-174-71-194.ngrok-free.app/api/call'
    # headers = {
    #     "ngrok-skip-browser-warning": "69420"
    # }
    payload = {
        'chatMessage': transcription,
        'isChatMessage': True,
        'isCallOngoing': True,
        'isCallEnded': False,
        'aiResponse': False
    }
    url = "http://localhost:4000/api/call"

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("POST request successful about message")
        else:
            print(f"POST request failed with status code {response.status_code} and message {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    for _ in range(3):
        try:
            res = model.generate_content([
                {'role': 'user', 'parts': [PROMPT]},
                {'role': 'model', 'parts': ["Ok sure, Ask your query!"]},
                {'role': 'user', 'parts': [transcription]}
            ])
            print("The AI generated response is: ", res)
            res = res.text
            payload = {
                'chatMessage': res,
                'isChatMessage': True,
                'isCallOngoing': True,
                'isCallEnded': False,
                'aiResponse': True,
            }
            url = "http://localhost:4000/api/call"
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print("POST request successful about message")
                else:
                    print(f"POST request failed with status code {response.status_code} and message {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            l.append(re.search(PATTERN, res, re.IGNORECASE).group(1).strip())
            break
        except Exception as e:
            print(f"Error in model generation: {e}")
            pass

    response = VoiceResponse()
    response.redirect(f'{URL}/webhooks/input')
    print(datetime.now() - s)
    return str(response)

if __name__ == '__main__':
    app.run(port=3000)
