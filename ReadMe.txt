# Multimodal Emotionally Aware Voice Cloning Agent

An intelligent, low-latency speech-to-speech companion that combines emotional intelligence with adaptive biographical memory to bridge the empathy gap in conversational systems. This application uses a dual-stream architecture to capture human sentiment, dynamically reference a local vector database, and reply in real time using high-fidelity zero-shot voice cloning.

---

##  Project Video Demonstration
A comprehensive 6-minute operational walk-through showcasing real-time audio capturing, live emotion classification context tracking, dynamic memory CRUD manipulation, and high-fidelity target voice cloning execution.

**[Watch the Project Demonstration Video (demo.mp4)](./demo.mp4)**

---

## 🛠 Project Tech Stack
* **Frontend:** Vanilla HTML5, CSS3, WebRTC MediaRecorder API
* **Backend Framework:** FastAPI (Python 3.10+)
* **AI Ear (ASR):** AssemblyAI (`universal-3-pro`)
* **AI Brain (NLP & RAG):** Groq API (`llama-3.1-8b-instant`), FAISS Vector DB
* **Emotion Engine:** HuggingFace Pipeline (`j-hartmann/emotion-english-distilroberta-base`)
* **AI Mouth (Voice Synthesis):** Coqui XTTS v2 via remote GPU Tunneling

---

##  Repository Folder Structure

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
Environment Build & Local Installation
Follow these steps sequentially to configure your local execution environment:

1. Clone the Workspace & Create Virtual Environment
Open your terminal (PowerShell/Bash) and initialize the active runtime workspace:

PowerShell
# Navigate to workspace and build project container
cd "C:\Users\TTS"

# Create an isolated Python environment
python -m venv tts_env

# Activate the virtual environment
# Windows PowerShell:
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& ".\tts_env\Scripts\Activate.ps1")
# Linux/macOS:
source tts_env/bin/activate
2. Install Backend Core Dependencies
Run the library installation command inside your active virtual environment:

PowerShell
pip install fastapi uvicorn requests python-dotenv transformers langchain-huggingface langchain-groq langchain-community faiss-cpu
Secret Configuration & API Access
Create a file named .env in the root directory. Paste the following configuration variables and fill in your keys directly without quotation marks:

Plaintext
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
HF_TOKEN=hf_your_actual_huggingface_write_token_here
ASSEMBLYAI_API_KEY=your_actual_assemblyai_api_key_here
NGROQ=your_actual_ngrok_auth_token_here
How to Obtain Access Keys:
Groq API Key: Register at the Groq Developers Console to access ultra-low-latency LPU inference.

HF Token: Create a HuggingFace account, navigate to Settings -> Tokens, and generate a token with Read access to pull down the distilroberta classifier.

AssemblyAI API Key: Sign up at the AssemblyAI dashboard to run the universal-3-pro engine.

Google Colab GPU Setup & Cloudflare Tunnel Linkage
Because running the state-of-the-art Coqui XTTS v2 model locally requires high-end VRAM, the execution loop shifts heavy computing workloads onto a free cloud-hosted remote GPU instance.

1. Configure Google Colab Workspace
Create or open notebooks/xtts_colab_server.ipynb.

Change runtime execution parameters to use the T4 GPU accelerator (Runtime -> Change runtime type -> T4 GPU).

The script boots an API listener wrapper inside the Colab cloud notebook and starts a public Cloudflare Tunnel connection using pycloudflared.

2. Link Bridging to app.py
When the Colab notebook finishes initialization, it will output a public proxy web link similar to this:
https://adrian-due-extra-equal.trycloudflare.com

Copy this public URL address from the Colab notebook output, open your local app.py file, and replace the global string mapping variable at the top:

Python
# PASTE YOUR ACTIVE COLAB URL HERE EACH TIME YOU REBOOT THE NOTEBOOK
COLAB_TTS_URL = "[https://your-active-cloudflare-url.trycloudflare.com](https://your-active-cloudflare-url.trycloudflare.com)"
Biography Data Handling & Real-Time CRUD
The system processes personal identity context files via local vector spaces:

Storage Mechanism: Structural text datasets are read directly from apj.txt.

RAG Pipeline Processing: RecursiveCharacterTextSplitter breaks text into chunks of 400 characters. These are converted into high-dimensional vectors by nomic-embed-text-v1.5 and stored in a local FAISS vector store.

Dynamic Modifiers (CRUD): The dashboard interface allows for instant database mutation. Calling the /api/memory/insert or /api/memory/delete endpoints alters the tracking file and instantly triggers reload_db() to refresh the active vector space configurations without taking the server offline.

Operational Output & Interaction Guidance
Run the system pipeline using your terminal window:

PowerShell
uvicorn app:app --reload
Open a browser page tracking http://127.0.0.1:8000 to access the interface.

1. Supported Input Formats
Voice Format (Interactive): Click the "Start Camera/Microphone" toggle button on the web interface dashboard. Speak clearly into your device. The WebRTC API streams audio components directly, exporting a temporary .wav file to the server for AssemblyAI processing.

Text Format (UI Standard): Type directly into the interface query inputs to submit requests without using microphone capture tracking.

2. Combined Output Formats
Once the server finishes processing conversational logic loops, it simultaneously updates two payload dimensions:

Text Response Presentation: The filtered text answer string is displayed inside the user dashboard alongside a calculated metric tag tracking the evaluated emotion (e.g., Joy, Sadness).

Voice Cloning Auditory Playback: The browser plays a high-fidelity .wav file synthesized by the remote GPU server. This speech track contains the exact vocal timbre and pitch characteristics extracted from the reference voice.wav profile asset.
