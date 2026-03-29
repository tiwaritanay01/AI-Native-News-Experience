# Aureum Terminal: Architecture & Logic Flow 🌊

The following diagram illustrates how **Aureum Terminal** orchestrates intelligence from the **User Persona** level down to the **Hardware Abstraction Layer (HAL)** and its resilient error-handling logic.

---

## 🏗️ The Intelligence Pipeline

```mermaid
graph TD
    subgraph User_Persona [User Personas]
        U1[Investive Analyst] --> Dash
        U2[Startup Founder] --> Dash
        U3[Hedge Fund Strategist] --> Dash
    end

    subgraph Frontend [Angular 17+ Dashboard]
        Dash[Centralized RxJS State] --> Brief[Story Briefing SSE]
        Dash --> Chat[Navigator Chat RAG]
        Dash --> Vid[Auto-Video Pipeline]
    end

    subgraph Backend [FastAPI / Hybrid Infrastructure]
        Brief --> HAL[Hardware Abstraction Layer]
        Chat --> HAL
        Vid --> HAL

        HAL -->|Priority 1: Zero-Latency| Groq[Groq LPU Clusters]
        HAL -->|Priority 2: Deep Context| Gemini[Gemini-1.5 API]
        HAL -->|Priority 3: Patterns| JAX[Local TPU/JAX Cluster]

        subgraph Resiliency [Resiliency & Error Handling]
            Groq -->|HTTP 429 Error| Retry[Retry Logic / 10m Window]
            Retry -->|Fail| Mock[Mock-Fallback Layer]
            Mock -->|Status: Simulated| Dash
        end
    end

    subgraph Tools [Tool Integration & External Data]
        JAX --> NSE[Jugaad-Data NSE Mirror]
        JAX --> GLB[Finnhub Global Market API]
        Groq --> VDB[ChromaDB Vector Search]
    end

    subgraph Final_Output [Intelligence Signals]
        Dash --> Out1[Market Readiness: +15%]
        Dash --> Out2[Information Alpha: High]
        Dash --> Out3[Zero-Noise Briefing: Done]
    end

    style Groq fill:#f96,stroke:#333,stroke-width:2px
    style HAL fill:#9cf,stroke:#333,stroke-width:2px
    style Mock fill:#f66,stroke:#333,stroke-width:2px
```

---

## 🛠 Flow Logic Deep-Dive

### 1. User Engagement (The Start)
Whether the persona is an **Investor** tracking market volatility or a **Founder** monitoring competitive shifts, the **Angular Dashboard** uses a synchronized `DashboardStateService` to ensure all UI cards (Hero, Radar, Navigator) update from a single source of truth.

### 2. The HAL Routing
Instead of hardcoding APIs, the backend uses a **Hardware Abstraction Layer (HAL)**. If character-by-character streaming is needed, the request is routed to the **Groq LPU**. If complex, high-context synthesis is required, it shifts to **Gemini**.

### 3. Resilience & Error Handling
To maintain **Production-Grade Uptime**, our system includes a specialized **Fallback Block**:
*   **Retry Logic**: Attempts 2-3 retries for minor timeouts.
*   **Mock-Fallback**: If the user reaches their Daily Rate Limit (`429`), the system instantly shifts to **Mock Intelligence Generation**. This ensures the UI remains functional and informative even during cloud-service outages.

### 4. Tool Integration
We built custom connectors for:
*   **`jugaad-data`**: Specifically for Indian NSE/BSE mirrors.
*   **`finnhub`**: For global NASDAQ and NYSE liquidity metrics.
*   **`ChromaDB`**: As our semantic vector storage for RAG-driven chat.
