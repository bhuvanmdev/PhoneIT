from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from os.path import join
import google.generativeai as genai
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import re
import time
from datetime import datetime as d
import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import translator 
import requests

# BATCH_SIZE=4
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# quantization = "4-bit"
# en_indic_ckpt_dir1 = "ai4bharat/indictrans2-en-indic-dist-200M"
# en_indic_tokenizer1, en_indic_model1 = initialize_model_and_tokenizer(en_indic_ckpt_dir1, "en-indic","4-bit",DEVICE=DEVICE)
# indic_en_ckpt_dir = "ai4bharat/indictrans2-indic-en-dist-200M"  # ai4bharat/indictrans2-indic-en-dist-200M
# indic_en_tokenizer, indic_en_model = initialize_model_and_tokenizer(indic_en_ckpt_dir, "indic-en", "4-bit",DEVICE=DEVICE)

translate = translator.Translate("ai4bharat/indictrans2-en-indic-dist-200M","ai4bharat/indictrans2-indic-en-dist-200M")


# from translate import libre_translate_text as lbt

dotenv_path = join(r"/home/abhyuday/Desktop/ML-Haako/caller/.env")
load_dotenv(dotenv_path)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
URL = os.getenv("URL")
TO_NUM = os.getenv("TO_NUM")
GKEY = os.getenv("GKEY")
LLM = os.getenv("LLM")
PROMPT = f"""You are a helpful AI voice agent who responds to user queries regarding government schemes based only from the given context. Please generate text output that is optimized for Text-to-Speech (TTS) models. Follow these guidelines to ensure clarity and ease of understanding:
1. Use Proper Grammar and Punctuation: Ensure that the text is grammatically correct and punctuated appropriately.
2. Avoid Emojis and Problamatic Special Characters: Do not include emojis, symbols, or any special characters that are not necessary for the content. This includes boldizing, intalics, and other formatting (i.e no "", ":" to be included).
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
Context:
"""
PATTERN = r"<say>(.*?)</say>"
PROMPT = f"""You are a helpful AI voice all agent who responds to user queries based on the given context. Please generate text output that is optimized for Text-to-Speech (TTS) models. Follow these guidelines to ensure clarity and ease of understanding:
1. Use Proper Grammar and Punctuation: Ensure that the text is grammatically correct and punctuated appropriately.
2. Avoid Emojis and Problamatic Special Characters: Do not include emojis, symbols, or any special characters that are not necessary for the content. This includes boldizing, intalics, and other formatting (i.e no "", ":" to be included).
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
Context:
"""
genai.configure(api_key=GKEY)

model = genai.GenerativeModel(LLM)

loader_neuro = PyPDFLoader("/home/abhyuday/Desktop/translator/Scheme Booklet 2022-23.pdf")
pages_neuro = loader_neuro.load_and_split()

# Define the path to the pre-trained model you want to use
modelPath = "sentence-transformers/all-MiniLM-l6-v2"

# Create a dictionary with model configuration options, specifying to use the CPU for computations
model_kwargs = {'device':'cpu'}

# Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
encode_kwargs = {'normalize_embeddings': False}

# Initialize an instance of HuggingFace
#Embeddings with the specified parameters
embeddings = HuggingFaceEmbeddings(
    model_name=modelPath,     # Provide the pre-trained model's path
    model_kwargs=model_kwargs, # Pass the model configuration options
    encode_kwargs=encode_kwargs # Pass the encoding options
)
splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=30)
documents = splitter.split_documents(pages_neuro)
db = FAISS.from_documents(documents, embeddings)

retriever = db.as_retriever(search_kwargs={"k":2})

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
# print("env values:", TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER, URL, TO_NUM, GKEY)
uuid = ''
l = []
k = 1
lang = "en-IN"
dic = {'1': 'en-IN', '2': 'hi-IN', '3': 'kn-IN', '4': 'bn-IN',"5":'ta-IN'}  # 0 style for kan and beng
call = s = None
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def call():
    global uuid,call
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
    gather.say('Press 1 for English')
    gather.say('हिन्दी के लिए 2 दबाएँ',language='hi-IN')
    gather.say('ಕನ್ನಡಕ್ಕಾಗಿ 3 ಒತ್ತಿರಿ',language='kn-IN')
    gather.say('বাংলার জন্য 4 টিপুন',language='bn-IN')
    gather.say('தமிழ் க்கு 5 அழுத்தவும்',language='ta-IN')
    response.append(gather)
    # print(f"\n\n\nstr:{response._str()},type:{type(response)},dir:{response.dir_()},raw:{response}\n\n\n")
    return str(response)

@app.route('/webhooks/input', methods=['POST'])
def handle_input():
    # print("Error occurred after handle input")
    global k, lang, s
    digits = request.values.get('Digits', None)
    if digits:
        l.append({1: 'Hello! When I stop speaking, please ask your query and wait for 3 seconds.', 2: 'नमस्कार। जब मैं बोलना बंद कर दूं, तो कृपया अपना प्रश्न पूछें और 3 सेकंड प्रतीक्षा करें।' , 3: 'ನಮಸ್ಕಾರ. ನಾನು ಮಾತನಾಡುವುದನ್ನು ನಿಲ್ಲಿಸಿದಾಗ, ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ ಮತ್ತು 3 ಸೆಕೆಂಡುಗಳ ಕಾಲ ಕಾಯಿರಿ.', 4: 'নমস্কার। আমি কথা বলা বন্ধ করলে, দয়া করে আপনার প্রশ্ন জিজ্ঞাসা করুন এবং 3 সেকেন্ড অপেক্ষা করুন।', 5:"ஹலோ! நான் பேசுவதை நிறுத்தும்போது, உங்கள் கேள்வியைக் கேட்டு 3 வினாடிகள் காத்திருக்கவும்." }.get(int(digits), 'Hello! When I stop speaking, please ask your question and wait for 3 seconds.'))
        lang = dic.get(digits, 'en-IN')
    response = VoiceResponse()
    if digits == '0':
        response.say('Goodbye')
    else:
        print(f"DONE {k}")
        response.say(l[-1], language=lang)
        gather = Gather(input="speech", language=lang, action=f'{URL}/webhooks/recordings', speech_timeout=3)
        # gather.say(l[-1], language=lang)
        response.append(gather)
        s = datetime.now()
    k += 1
    print(response.__str__(), response.__dir__())
    return str(response)

@app.route('/webhooks/recordings', methods=['POST'])
def handle_recordings():
    # print("Error occurred after this")
    print(request, request.values)
    
    transcription = request.values.get('SpeechResult')
    print("adfal;kdfja; Transcription",transcription)
    # print(f"\n\nTranslation: {transcription}\n\n")

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

    if lang!="en-IN":
        transcription=translate.translate(transcription,lang,0)
    # transcription = lbt(transcription, lang.split('-')[0],'en')
    # transcription = "can you tell me more about an elephant?"
    con=""
    for x in retriever.get_relevant_documents(transcription): #trans
        con += x.page_content + '\n'
    PROMPT += con
    print(f"\n\nTranslation: {transcription}\n\n")
    print(f"\n\nTranscription: {transcription}\n\n")
    
    

    for _ in range(3):
        try:
            res = model.generate_content([
                {'role': 'user', 'parts': [PROMPT]},
                {'role': 'model', 'parts': ["Ok sure, Ask your query!"]},
                {'role': 'user', 'parts': [transcription]}
            ])
            print("The AI generated response is: ", res)
            res = res.text
            res = re.search(PATTERN, res,re.IGNORECASE).group(1).strip()
            if lang!="en-IN":
                res=translate.translate(res,lang,1)
            # res = lbt(re.search(PATTERN, res,re.IGNORECASE).group(1).strip(), 'en',lang.split('-')[0])
            print(res)
            l.append(res)
            payload = {
                'chatMessage': res,
                'isChatMessage': True,
                'isCallOngoing': True,
                'isCallEnded': False,
                'aiResponse': True,
            }
            print("Payload: ", payload)
            url = "http://localhost:4000/api/call"
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print("POST request successful about message with AI response flag set to True")
                else:
                    print(f"POST request failed with status code {response.status_code} and message {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            # l.append(re.search(PATTERN, res, re.IGNORECASE).group(1).strip())
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