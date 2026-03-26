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

# 3. High-Performance SSE Event Generator
async def sse_event_generator(prompt: str, cluster_id: int) -> AsyncGenerator[str, None]:
    try:
        # Initial status event to trigger the UI immediately
        yield f"data: {json.dumps({'status': 'initializing', 'engine': 'JAX-TPU-v5e-1'})}\n\n"
        await asyncio.sleep(0.1)
        
        # Explicit start token to clear 'Decoding stream...' text
        yield "data: [START]\n\n"
        await asyncio.sleep(0.1)

        # Stream the actual TPU tokens token-by-token
        async for chunk in stream_jax_inference(prompt, cluster_id):
            if chunk:
                yield f"data: {chunk}\n\n"
                # Small wait to ensure chunks are pushed individually
                await asyncio.sleep(0.02)  

        # Final completion signal
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

# 4. Attach High-Performance Streaming Endpoints to the existing app
@app.post("/api/agents/streaming-briefing")
async def stream_briefing(request: Request):
    """Refactored endpoint specifically for real-time news briefings on TPU v5e-1."""
    body = await request.json()
    cluster_id = body.get("cluster_id", 0)
    prompt = body.get("prompt", "Generate a deep news briefing.")

    # X-Accel-Buffering: no is CRITICAL for ngrok streaming to work immediately
    return StreamingResponse(
        sse_event_generator(prompt, cluster_id),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"}
    )

@app.get("/ingest")
def ingest_news():
    """Restored news ingestion logic."""
    articles = fetch_business_news()
    store_articles(articles)
    return {"status": "success", "message": "news stored"}

@app.get("/api/health")
async def health_check():
    """Endpoint for Colab diag logic."""
    return {"status": "online", "hardware": "TPU_v5e-1", "engine": "JAX"}

# 5. Master Entry Point
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
