import os
import time
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv

# LangChain & HuggingFace
from transformers import pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

# --- 1. CONFIGURATION ---
load_dotenv()
ASSEMBLYAI_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

# ⚠️ VERY IMPORTANT: Make sure this is your ACTIVE Colab URL!
COLAB_TTS_URL = "https://adrian-due-extra-equal.trycloudflare.com"

app = FastAPI()

# --- AUTO-UPLOAD VOICE ON STARTUP ---
@app.on_event("startup")
def upload_reference_voice():
    print("🔄 Checking Colab connection and voice reference...")
    if os.path.exists("voice.wav"):
        try:
            with open("voice.wav", "rb") as f:
                res = requests.post(f"{COLAB_TTS_URL}/upload", files={"file": f})
            if res.status_code == 200:
                print("✅ Reference 'voice.wav' successfully uploaded to Colab GPU!")
            else:
                print(f"⚠️ Colab rejected the upload. Is your COLAB_TTS_URL correct? ({res.text})")
        except Exception as e:
            print(f"❌ Failed to connect to Colab. Make sure it is running! Error: {e}")
    else:
        print("⚠️ 'voice.wav' not found on startup. You will need to add a person via the UI.")

# --- 2. RAG MEMORY SYSTEM (CRUD) ---
FILE_PATH = "apj.txt"
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w", encoding="utf-8") as f: f.write("Initial entry.")

def load_db():
    with open(FILE_PATH, "r", encoding="utf-8") as f: content = f.read()
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    docs = [Document(page_content=t.strip()) for t in splitter.split_text(content) if t.strip()]
    if not docs:
        docs = [Document(page_content="Empty memory.")]
    embedding = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1.5", model_kwargs={'trust_remote_code': True})
    return FAISS.from_documents(docs, embedding)

vectorstore = load_db()

def reload_db():
    global vectorstore
    vectorstore = load_db()

# --- 3. AI BRAIN & EMOTION SETUP ---
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.5)

template_text = "Context: {context}\nQuestion: {question}\nAnswer clearly and concisely."
if os.path.exists("p_template.txt"):
    with open("p_template.txt", "r", encoding="utf-8") as f: template_text = f.read()

prompt = PromptTemplate(input_variables=["context", "question"], template=template_text)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff", chain_type_kwargs={"prompt": prompt})

# ==========================================
# API ENDPOINTS
# ==========================================

@app.get("/")
def serve_ui():
    """Serves your HTML frontend."""
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# --- NEW: UPLOAD PERSONA ENDPOINT ---
@app.post("/api/persona")
async def add_persona(
    name: str = Form(...),
    voice_file: UploadFile = File(...),
    bio_file: UploadFile = File(...)
):
    """Receives new voice and bio files from the UI, updates backend, and pushes to Colab."""
    try:
        # 1. Save and reload the text memory (Bio)
        bio_content = await bio_file.read()
        with open(FILE_PATH, "wb") as f:
            f.write(bio_content)
        reload_db()
        print(f"✅ RAG Database re-indexed for {name}")

        # 2. Save the voice locally
        voice_content = await voice_file.read()
        with open("voice.wav", "wb") as f:
            f.write(voice_content)

        # 3. Push the new voice to the Colab GPU
        with open("voice.wav", "rb") as f:
            res = requests.post(f"{COLAB_TTS_URL}/upload", files={"file": f})
            if res.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Colab rejected the voice: {res.text}")
        
        return {"status": "Success", "message": f"Persona '{name}' successfully loaded!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Takes microphone audio from UI, sends to AssemblyAI, returns text."""
    temp_file = "temp_mic.wav"
    with open(temp_file, "wb") as f: f.write(await file.read())
    
    if not ASSEMBLYAI_KEY:
        raise HTTPException(status_code=500, detail="ASSEMBLYAI_API_KEY is missing!")

    headers = {"authorization": ASSEMBLYAI_KEY}
    
    with open(temp_file, "rb") as f:
        upload_response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, data=f)
        
    if upload_response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"AssemblyAI Upload Error: {upload_response.text}")
        
    audio_url = upload_response.json().get("upload_url")
    
    json_data = {"audio_url": audio_url, "speech_models": ["universal-3-pro"]}
    transcript_response = requests.post("https://api.assemblyai.com/v2/transcript", json=json_data, headers=headers)
    res_json = transcript_response.json()
    
    if "id" not in res_json:
        raise HTTPException(status_code=500, detail=f"AssemblyAI Error: {res_json}")
        
    tid = res_json["id"]
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{tid}"
    
    while True:
        res = requests.get(polling_endpoint, headers=headers).json()
        if res["status"] == "completed": return {"text": res["text"]}
        elif res["status"] == "error": raise HTTPException(status_code=500, detail=f"Transcription Error: {res.get('error')}")
        time.sleep(1)

@app.post("/api/chat")
async def chat_with_brain(text: str = Form(...)):
    """Takes transcribed text, detects emotion, asks Groq/FAISS, returns answer."""
    emo_res = emotion_model(text)[0][0]
    emotion = emo_res['label']
    
    query_with_emo = f"{text}\n\n(User Emotion: {emotion})"
    answer = qa_chain.invoke({"query": query_with_emo})["result"]
    return {"answer": answer, "emotion": emotion}

@app.post("/api/tts")
async def generate_voice(text: str = Form(...)):
    """Sends the LLM answer to Colab XTTS and returns the audio file."""
    headers = {"ngrok-skip-browser-warning": "true"}
    
    try:
        res = requests.post(f"{COLAB_TTS_URL}/generate", json={"text": text}, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reach Colab. Is the URL correct? Error: {str(e)}")
        
    if res.status_code == 200:
        with open("output_speech.wav", "wb") as f: f.write(res.content)
        return FileResponse("output_speech.wav", media_type="audio/wav")
        
    raise HTTPException(status_code=500, detail=f"XTTS Generation failed. Server returned: {res.text}")

# --- CRUD MEMORY ENDPOINTS ---
@app.post("/api/memory/insert")
async def mem_insert(text: str = Form(...)):
    with open(FILE_PATH, "a", encoding="utf-8") as f: f.write("\n\n" + text)
    reload_db()
    return {"status": "Inserted"}

@app.post("/api/memory/delete")
async def mem_delete(query: str = Form(...)):
    results = vectorstore.similarity_search_with_score(query, k=1)
    if not results: return {"status": "Not found"}
    target = results[0][0].page_content
    
    with open(FILE_PATH, "r", encoding="utf-8") as f: data = f.read()
    with open(FILE_PATH, "w", encoding="utf-8") as f: f.write(data.replace(target, ""))
    reload_db()
    return {"status": f"Deleted: {target[:30]}..."}
