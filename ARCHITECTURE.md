# Aureum Terminal: Technical Architecture 🏗️

The **Aureum Terminal** is designed as a **Hybrid Neural Infrastructure** that offloads heavy inference to cloud-based LPUs (Groq) and Tensor Processing Units (TPU) while maintaining a lightweight, high-performance Angular frontend.

---

## 1. High-Level Hub (Mermaid Visualization)
```mermaid
graph TD
    subgraph Frontend (Angular Dashboard)
        UI[App Components] --> State[Centralized State Service]
        State --> Service[News Service]
        SSE[SSE Stream Handler] --> UI
    end
    
    subgraph Backend (FastAPI on Colab/Jax)
        API[FastAPI Router] --> HAL[Hardware Abstraction Layer]
        HAL -->|Priority 1: Speed| Groq[Groq LPU Clusters]
        HAL -->|Priority 2: Context| Gemini[Gemini 1.5 Pro API]
        HAL -->|Priority 3: Patterns| TPU[Local JAX TPU Model]
        
        API --> VDB[ChromaDB Vector Store]
        API --> Market[Hybrid Market Data Engine]
    end
    
    subgraph Data & Signal Sources
        Market --> NSE[Jugaad-Data Mirrors]
        Market --> Global[Finnhub Core API]
        Scraper[News Ingestion Pipeline] --> VDB
    end
```

---

## 2. The Hybrid HAL (Hardware Abstraction Layer)
The core of our intelligence architecture is the **HAL**, which intelligently routes tasks based on computational cost and latency requirements:
*   **Groq Mode (LPU Cluster)**: The default for chat and briefings. We use Groq's specialized **Language Processing Units** for character-by-character "Zero-Latency" streaming.
*   **Gemini Mode (Multimodal API)**: Used for complex story synthesis and deep cross-article reasoning where context length is a priority.
*   **JAX/TPU Mode (Local Clusters)**: Used for semantic article clustering and vector dimension reduction in the background.
*   **Mock-Fallback Layer**: A critical production feature that automatically serves simulated high-fidelity data if cloud API quotas (429) are exhausted, maintaining a flawless UX.

---

## 3. Data Pipeline: The Hybrid Market Engine
We developed a sophisticated **Regex Routing Logic** to bridge disparate financial markets without the need for multiple heavy subscriptions:
```python
# Conceptual Logic in app/services/market_service.py
if symbol.endswith('.NS'):
    return get_indian_market_data(symbol) # via Jugaad-Data (NSE Mirror)
else:
    return get_global_market_data(symbol) # via Finnhub API (NASDAQ/NYSE)
```
This ensures we provide sub-second financial correlation for both local Indian stakeholders and global investors in a single story node.

---

## 4. Frontend State & Synchronization
To ensure a cohesive experience, the Angular frontend utilizes a **Centralized Dashboard State Service**:
*   **Synchronized UI**: When the user clicks on a news node, the **Navigator**, **Story Arc**, **Impact Radar**, and **Hero Cards** all update simultaneously based on a single source of truth.
*   **RxJS Token Streaming**: The News Service uses an RxJS `Observable` to handle Server-Sent Events (SSE). This allows tokens to "bubble up" to the UI as they arrive, bypassing standard HTTP wait times.

---

## 5. Automated Video Shorts Pipeline
The `/api/story/{id}/video` endpoint triggers an asynchronous pipeline:
1.  **Scripting**: Groq writes a viral-style script.
2.  **Voice**: High-fidelity neural TTS synthesis.
3.  **Visuals**: Pollinations API generates context-aware frames; Picsum serves as the high-availability fallback.
4.  **Composition**: `moviepy` assembles the final MP4 on the backend disk for static serving.
