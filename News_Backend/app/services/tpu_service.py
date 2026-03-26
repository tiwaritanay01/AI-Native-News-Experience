"""
Streaming Bridge — Wraps the HAL's `stream_tokens` for SSE consumption.
This is what main.py calls for the real-time briefing endpoint.
"""
from app.services.hardware_engine import stream_tokens, get_hardware_type


async def stream_jax_inference(prompt: str, cluster_id: int):
    """
    Async generator that yields tokens for SSE streaming.
    Internally uses the HAL to work on TPU, GPU, CPU, or Mock.
    
    The function name is kept as `stream_jax_inference` for backwards 
    compatibility with main.py imports.
    """
    hw = get_hardware_type()
    print(f"🚀 [{hw}] Streaming inference for cluster {cluster_id}")

    async for token in stream_tokens(prompt):
        yield token
