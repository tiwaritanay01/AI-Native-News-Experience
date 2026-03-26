import uvicorn
import json
import asyncio
from typing import AsyncGenerator
from fastapi import Request
from fastapi.responses import StreamingResponse

# 1. Import the existing API instance which contains all original routes (/stories, /story-of-day, etc.)
from app.api.news_api import app 

# 2. Import project services
from app.ingestion.news_ingestion import fetch_business_news
from app.services.store_articles import store_articles
from app.services.tpu_service import stream_jax_inference
from app.services.hardware_engine import initialize_engine, get_hardware_type

# 3. Initialize the Hardware Abstraction Layer on module load
#    This probes for TPU → GPU → CPU → Mock automatically
import os
MODEL_NAME = os.environ.get("MODEL_NAME", "google/gemma-2b")
initialize_engine(MODEL_NAME)

# 4. High-Performance SSE Event Generator
async def sse_event_generator(prompt: str, cluster_id: int) -> AsyncGenerator[str, None]:
    try:
        hw = get_hardware_type()
        # Initial status event to trigger the UI immediately
        yield f"data: {json.dumps({'status': 'initializing', 'engine': hw})}\n\n"
        await asyncio.sleep(0.1)
        
        # Explicit start token to clear 'Decoding stream...' text
        yield "data: [START]\n\n"
        await asyncio.sleep(0.1)

        # Stream the actual tokens token-by-token (TPU/GPU/CPU/Mock)
        async for chunk in stream_jax_inference(prompt, cluster_id):
            if chunk:
                yield f"data: {chunk}\n\n"
                await asyncio.sleep(0.02)  

        # Final completion signal
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

# 5. Attach Streaming Endpoints to the existing app
@app.post("/api/agents/streaming-briefing")
async def stream_briefing(request: Request):
    """Real-time news briefing — works on TPU, GPU, CPU, or Mock."""
    body = await request.json()
    cluster_id = body.get("cluster_id", 0)
    prompt = body.get("prompt", "Generate a deep news briefing.")

    return StreamingResponse(
        sse_event_generator(prompt, cluster_id),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"}
    )

@app.get("/ingest")
def ingest_news():
    """News ingestion endpoint."""
    articles = fetch_business_news()
    store_articles(articles)
    return {"status": "success", "message": "news stored"}

@app.get("/api/health")
async def health_check():
    """Dynamic health check that reports actual hardware."""
    hw = get_hardware_type()
    return {"status": "online", "hardware": hw, "engine": "HAL-Hybrid"}

# 6. Master Entry Point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
