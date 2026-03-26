import asyncio
import json
import os
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.news_api import app
from app.services.tpu_service import stream_jax_inference
from app.agents.story_agent import get_all_stories

# Re-initialize main app to support Streaming & Async
app = FastAPI(title="AI-Native News - High Performance TPU Edition")

# CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared cluster id state (optional cache)
_LATEST_CLUSTER_ID = 0

async def sse_event_generator(prompt: str, cluster_id: int) -> AsyncGenerator[str, None]:
    """
    Wraps the TPU JAX inference engine into an SSE-compatible stream.
    """
    try:
        # Initial status event
        yield f"data: {json.dumps({'status': 'initializing', 'engine': 'JAX-TPU-v5e-1'})}\n\n"
        await asyncio.sleep(0.1)

        # Stream the actual inference content chunk-by-chunk
        async for chunk in stream_jax_inference(prompt, cluster_id):
            # Format as SSE data:
            yield f"data: {chunk}\n\n"
            # Yield control back to event loop
            await asyncio.sleep(0)  

        # Send completion event
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.get("/")
async def home():
    return {"status": "online", "hardware": "TPU v5e-1", "engine": "JAX", "api": "Streaming SSE Ready"}

@app.post("/api/agents/streaming-briefing")
async def stream_briefing(request: Request):
    """
    Main endpoint for real-time streaming AI briefings.
    Uses POST to allow large prompt context or IDs.
    """
    body = await request.json()
    cluster_id = body.get("cluster_id", 0)
    prompt = body.get("prompt", "Generate a deep news briefing.")

    return StreamingResponse(
        sse_event_generator(prompt, cluster_id),
        media_type="text/event-stream"
    )

@app.get("/stories")
def stories():
    return get_all_stories()

if __name__ == "__main__":
    import uvicorn
    # Use multiple workers if needed, but usually 1 on TPU context to maintain XLA handles
    uvicorn.run(app, host="0.0.0.0", port=8000)
