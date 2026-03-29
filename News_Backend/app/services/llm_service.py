"""
Unified LLM Service — All agents import `generate_llm_response` from here.
Internally routes to the Hardware Abstraction Layer (HAL) which handles
TPU / GPU / CPU / Mock transparently.
"""
from app.services.hardware_engine import generate_response, get_hardware_type


_initialized = False

def _ensure_initialized():
    global _initialized
    if not _initialized:
        from app.services.hardware_engine import initialize_engine
        initialize_engine()
        _initialized = True

def generate_llm_response(prompt: str, model: str = "llama3") -> str:
    """
    Single entry point for all synchronous agent LLM calls.
    Ensures the hardware engine is initialized exactly once.
    """
    _ensure_initialized()
    hw = get_hardware_type()
    # Mask prompt for cleaner logs
    summary = prompt.strip()[:60].replace('\n', ' ')
    print(f"🚀 [{hw}] Inference triggered for pattern: {summary}...")
    return generate_response(prompt)