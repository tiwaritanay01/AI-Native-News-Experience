# Aureum Terminal: AI-Native News Experience 🚀

**Aureum Terminal** is a production-grade news orchestration platform that transforms static headlines into interactive, AI-driven intelligence. Built by the **Aureum Terminal Team**, it is optimized for the hyper-fast financial and tech sectors, bridging the gap between raw data and human-centric story arcs.

---

## 🌟 Our Vision: "Beyond the Headline"
Most news apps are just lists of text. We built an **Intelligence Terminal**. We leverage high-speed **Groq LPU (Language Processing Unit)** clusters and multimodal synthesis to:
*   **Cluster** messy, conflicting reports into unified Story Arcs.
*   **Synthesize** deep briefings in real-time with **Zero-Latency Intelligence**.
*   **Predict** narrative trajectories using predictive financial modeling.
*   **Automate** viral short-form video explainers for complex stories.

---

## 🛠 Features for the Hackathon Judge

### 1. Neural Story Briefing (Live SSE Streaming)
Our system uses **Server-Sent Events (SSE)** to bypass the traditional "waiting for LLM" bottleneck. Tokens are pushed to the UI character-by-character as they are generated, providing a real-time "typing" experience that feels alive and responsive.

### 2. AI News Navigator (Cognitive Chat RAG)
Don't just read the news—**interrogate it**. Our custom LLM agent allows you to ask deep questions about a story cluster. We use **Retrieval-Augmented Generation (RAG)** to ground every answer in source-verified article data.

### 3. Predictive Story Arc Tracker
Visualizes the narrative trajectory. It doesn't just show the past; it **predicts "What to watch next"** based on a momentum-weighted vector of current sentiment and article volume.

### 4. Vernacular Intel Engine (Regional Language Support)
Bridging the digital divide. Aureum can instantly localize complex financial news into regional languages (starting with Hindi) while maintaining technical accuracy and a professional editorial tone.

### 5. Multi-Market Ticker (Hybrid NSE-Finnhub)
Real-time financial status tracking. We built a **Hybrid Market Engine** that intelligently routes data: if a story mentions an Indian stock (`RELIANCE.NS`), it fetches from **Jugaad-Data**; for global tickers (`AAPL`), it hits the **Finnhub Global API**.

### 6. Video Explainer Pipeline (Auto-Shorts)
Turn any complex story into a 30s video short:
*   **Script**: LPU-accelerated Llama 3.3.
*   **Voice**: High-fidelity Neural TTS.
*   **Images**: Generative context-aware imagery (Pollinations/Picsum).
*   **Assembly**: Multi-threaded `moviepy` composition.

---

## 📺 Project Demos & Presentation

The following folder contains full working prototype videos showcasing the **Zero-Latency Groq Engine** and the **Resilient Mock-Fallback layer**:

🔗 **[Aureum Terminal: Working Model & Final Pitch (Google Drive)]([https://drive.google.com/drive/folders/1yO7nk_QvUwVKaCTQUwbTKS1AeyyclYKT?usp=sharing])**

### **Context for the Demo Videos:**
*   **Final Prototype**: Showcases the complete, high-speed end-to-end user journey across the News Intelligence Terminal.
*   **Groq API / Resiliency Showcase**: Our latest videos intentionally demonstrate the application's behavior when **Groq API Rate Limits (429)** are hit. You will notice the Terminal seamlessly switching to its internal **High-Fidelity Mock Engine**, ensuring the judges can always see the UI and data flow even during cloud-service outages.

---

## ⚡ Hardware Scaling & Compute Profile

The **Aureum Terminal** is architected to scale dynamically based on the available hardware:

| Feature | Primary Compute | Why? |
| :--- | :--- | :--- |
| **Navigator Chat / SSE Briefing** | **Any (API-Driven)** | These features are offloaded to **Groq LPU Clusters**, requiring zero local GPU/TPU power. |
| **Story Arc Tracking** | **CPU / TPU-Optimized** | Uses lightweight JAX-based interpolation; runs fast on CPU, but scales instantly on **TPU v5e**. |
| **Neural Clustering (HDBSCAN)** | **TPU / GPU Required** | Semantic clustering of 100+ articles requires high-density matrix math; **TPU-Agnostic JAX** is used for "Heavy Lifting" here. |
| **Video Production Pipeline** | **GPU Recommended** | `MoviePy` uses multi-core CPU by default, but utilizes **NVIDIA T4/A100** for hardware-accelerated encoding and generative frame synthesis. |
| **Market Engine & Dashboard UI** | **Standard CPU** | Highly optimized Angular state and Python-regex routing; runs flawlessly on any consumer-grade CPU. |

---

## 🏗 Technical Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Angular 17.1+, RxJS (Reactive State), Tailwind CSS |
| **Backend** | FastAPI (Python 3.10+), Uvicorn |
| **LLM Inference** | **Groq LPU** (Zero-Latency), Gemini-1.5-Flash |
| **Vector Engine** | ChromaDB (Article storage & Semantic Search) |
| **Compute Integration** | Hybrid Cloud (JAX/TPU-ready Backend) |
| **Tunnels** | Ngrok for secure, hybrid cloud-to-local communication |

---

## 🚀 Setup Walkthrough (for Hackathon Judges)

### **Step 1: The Backend (Cloud Engine)**
We use a separate resource account to run the high-performance AI backend in Google Colab.

1.  Open the [Colab Backend Script](https://colab.research.google.com/drive/1_vK7N8BvD2O3D5_I7fH5Z5G_9xYc6v8J),(https://drive.google.com/drive/folders/1svnsxXQxfppd5negECw1cWTitLadNNQB?usp=sharing),(https://colab.research.google.com/drive/11ILMT4YXMabAtNHXOwwGpHm-RzGWxzkQ?usp=sharing). (try any of 3 links)
2.  Enable **Secrets** (Key icon 🔑):
    *   `GROQ_API_KEY`, `FINNHUB_API_KEY`, `NGROK_AUTH_TOKEN`.
3.  Click **Runtime -> Run All**.
4.  Copy the **Live API URL** from the output (e.g., `https://hyper-natural-...ngrok-free.dev`).

### **Step 2: The Frontend (Local Machine)**
1.  Open `src/app/services/news.service.ts` in the provided repository.
2.  Update the `public api` property with your **Ngrok URL**.
3.  Run `npm install` followed by `ng serve -o`.
4.  **Login**: Use any test account to enter the dashboard.

---

## ⚠️ Troubleshooting & Resilience
*   **Rate Limits (429)**: To ensure UI stability, we implemented a **Mock-Fallback Layer**. If the Groq or Gemini APIs reach their token limits, the terminal automatically switches to high-quality simulated "Deep Intelligence" data based on the cluster's core themes.
*   **API Conflicts**: Ensure that your `Ngrok URL` is correctly pasted and that no trailing slashes exist in the URL string.

---

## 👨‍💻 Team: Aureum Terminal Team
### *Redefining News for the AI-Native Era.*
