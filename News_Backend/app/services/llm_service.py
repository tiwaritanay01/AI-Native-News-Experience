"""
Unified LLM Service — All agents import `generate_llm_response` from here.
Internally routes to the Hardware Abstraction Layer (HAL) which handles
TPU / GPU / CPU / Mock transparently.
"""
from app.services.hardware_engine import generate_response, get_hardware_type


def generate_llm_response(prompt: str, model: str = "llama3") -> str:
    """
    Single entry point for all synchronous agent LLM calls.
    Backwards-compatible with every service that previously imported this.
    """
    hw = get_hardware_type()
    print(f"🚀 [{hw}] Inference triggered for prompt: {prompt[:50]}...")
    return generate_response(prompt)