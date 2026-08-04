> **NOTE:** THIS PROJECT IS A PROTOTYPE-LEVEL PROJECT FEATURING FULLY WORKING MODELS UTILIZING LOCAL SYSTEM RESOURCES AND FREE-TIER OPEN-SOURCE INFRASTRUCTURE.

---

# Multimodal Emotionally Aware Voice Cloning Agent 🎙️🧠🎭

An intelligent, low-latency speech-to-speech companion that combines emotional intelligence with adaptive biographical memory to bridge the empathy gap in conversational AI systems. This application uses a dual-stream architecture to capture human sentiment, dynamically reference a local vector database using Retrieval-Augmented Generation (RAG), and reply in real time using high-fidelity zero-shot voice cloning.

---

## 🎥 Project Video Demonstration

A comprehensive 6-minute operational walk-through showcasing real-time audio capturing, live emotion classification, context tracking, dynamic memory CRUD manipulation, and high-fidelity target voice cloning execution.

[![Watch the Project Demonstration Video](./demo.mp4)](./demo.mp4)

---

## 🛠️ Tech Stack

* **Frontend:** Vanilla HTML5, CSS3, WebRTC MediaRecorder API
* **Backend Framework:** FastAPI (Python 3.10+)
* **AI Ear (ASR):** AssemblyAI (`universal-3-pro`)
* **AI Brain (NLP & RAG):** Groq API (`llama-3.1-8b-instant`), FAISS Vector DB
* **Emotion Engine:** HuggingFace Pipeline (`j-hartmann/emotion-english-distilroberta-base`)
* **AI Mouth (Voice Synthesis):** Coqui XTTS v2 via remote GPU Tunneling (Cloudflare)

---

## 📁 Repository Folder Structure

Organize your workspace directory exactly as follows before staging deployment files:

```text
Emotionally-Aware-Voice-Agent/
│
├── notebooks/
│   └── xtts_colab_server.ipynb # Remote GPU backend setup script
│
├── .env.example                # Template file for secret keys
├── .gitignore                  # Prevents tracking heavy/private artifacts
├── README.md                   # Complete repository documentation
├── app.py                      # FastAPI server orchestration engine
├── index.html                  # Monolithic dark-mode dashboard UI
├── apj.txt                     # Active text biographical database
├── voice.wav                   # Target cloning reference audio file
└── demo.mp4                    # 6-minute project demonstration video
⚡ Environment Build & All-in-One Local Setup
All-in-One Automated Setup (Copy & Paste)
You can run these consolidated block commands depending on your operating system to build the environment, install dependencies, and create template files automatically.

Windows (PowerShell)
PowerShell
# Create folder, initialize virtual environment, install dependencies, and create .env file
mkdir Emotionally-Aware-Voice-Agent; cd Emotionally-Aware-Voice-Agent
python -m venv tts_env
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
.\tts_env\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install fastapi uvicorn requests python-dotenv transformers langchain-huggingface langchain-groq langchain-community faiss-cpu
New-Item -ItemType File -Name .env -Force
Add-Content -Path .env -Value "GROQ_API_KEY=gsk_your_actual_groq_api_key_here`nHF_TOKEN=hf_your_actual_huggingface_write_token_here`nASSEMBLYAI_API_KEY=your_actual_assemblyai_api_key_here`nNGROQ=your_actual_ngrok_auth_token_here"
Linux / macOS (Bash)
Bash
# Create folder, initialize virtual environment, install dependencies, and create .env file
mkdir -p Emotionally-Aware-Voice-Agent && cd Emotionally-Aware-Voice-Agent
python3 -m venv tts_env
source tts_env/bin/activate
python3 -m pip install --upgrade pip
pip install fastapi uvicorn requests python-dotenv transformers langchain-huggingface langchain-groq langchain-community faiss-cpu
cat << 'EOF' > .env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
HF_TOKEN=hf_your_actual_huggingface_write_token_here
ASSEMBLYAI_API_KEY=your_actual_assemblyai_api_key_here
NGROQ=your_actual_ngrok_auth_token_here
EOF
🔑 Secret Configuration & API Access
Fill in your actual API keys inside your newly generated .env file without quotation marks:

Code snippet
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
HF_TOKEN=hf_your_actual_huggingface_write_token_here
ASSEMBLYAI_API_KEY=your_actual_assemblyai_api_key_here
NGROQ=your_actual_ngrok_auth_token_here
How to Obtain Access Keys:
Groq API Key: Register at the Groq Developers Console to access ultra-low-latency LPU inference.

HF Token: Create a HuggingFace account, navigate to Settings -> Tokens, and generate a token with Read access to download the distilroberta classifier.

AssemblyAI API Key: Sign up at the AssemblyAI Dashboard to run the universal-3-pro engine.

☁️ Google Colab GPU Setup & Cloudflare Tunnel Linkage
Running the state-of-the-art Coqui XTTS v2 model locally requires significant GPU VRAM. The system offloads heavy voice synthesis workloads to a free cloud-hosted remote GPU instance.

1. Configure Google Colab Workspace
Create or open notebooks/xtts_colab_server.ipynb.

Change runtime execution parameters to use the T4 GPU accelerator (Runtime -> Change runtime type -> T4 GPU).

Run the notebook to boot an API listener wrapper inside Colab and expose a public Cloudflare Tunnel via pycloudflared.

2. Link Tunnel to app.py
When the Colab notebook finishes initialization, it will output a public proxy link (e.g., https://your-active-cloudflare-url.trycloudflare.com).

Copy this public URL address from the Colab output, open your local app.py file, and update the global configuration variable at the top:

Python
# PASTE YOUR ACTIVE COLAB URL HERE EACH TIME YOU REBOOT THE NOTEBOOK
COLAB_TTS_URL = "[https://your-active-cloudflare-url.trycloudflare.com](https://your-active-cloudflare-url.trycloudflare.com)"
🧠 Biography Data Handling & Real-Time CRUD
The system processes personal identity context files via local vector spaces:

Storage Mechanism: Structural text datasets are read directly from apj.txt.

RAG Pipeline Processing: RecursiveCharacterTextSplitter breaks text into 400-character chunks, converts them into high-dimensional vectors via nomic-embed-text-v1.5, and stores them in a local FAISS vector store.

Dynamic Modifiers (CRUD): The dashboard interface allows instant database mutations. Calling /api/memory/insert or /api/memory/delete alters apj.txt and instantly triggers reload_db() to refresh the active vector space configurations without taking the server offline.

🚀 Operational Output & Execution
Start the local orchestration engine:

Bash
uvicorn app:app --reload
Open your browser and navigate to http://127.0.0.1:8000 to open the interface dashboard.

1. Supported Input Formats
Voice Format (Interactive): Click Start Camera/Microphone on the dashboard and speak into your device. The WebRTC MediaRecorder API streams audio and exports a temporary .wav file to the server for AssemblyAI transcription.

Text Format (UI Standard): Type directly into the interface query input box to submit requests directly without microphone input.

2. Combined Output Formats
When a conversational turn completes, the server updates two output dimensions simultaneously:

Text Response Presentation: The filtered textual answer string displays on the dashboard alongside the evaluated emotion metric (e.g., Joy, Sadness, Neutral).

Voice Cloning Auditory Playback: The browser streams a high-fidelity .wav file synthesized by the remote GPU server, matching the vocal timbre and pitch characteristics extracted from the reference voice.wav profile asset.


***

<ElicitationsGroup message="What would you like to do next?">
<Elicitation label="Generate a Dockerfile for the FastAPI server" query="Generate a Dockerfile for the FastAPI voice agent" query_intent="CLICKABLE_SUGGESTION" />
<Elicitation label="Add a Streamlit UI for the voice cloning agent" query="Create a Streamlit dashboard for the voice cloning agent" query_intent="CLICKABLE_SUGGESTION" />
<Elicitation label="Write unit tests for the FastAPI audio endpoint" query="Write pytest tests for FastAPI audio upload" query_intent="CLICKABLE_SUGGESTION" />
</ElicitationsGroup>
