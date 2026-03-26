"""
Hardware Abstraction Layer (HAL) for AI-Native News Experience.
Dynamically detects TPU v5e / NVIDIA T4 GPU / CPU and initializes the 
correct inference engine. All other services call this module — they never
need to know what hardware is running underneath.
"""
import os
import sys
import asyncio

# ─── Global State ───────────────────────────────────────────────────
_engine = None          # Will hold the initialized model/tokenizer/device
_hardware_type = "MOCK" # "TPU", "CUDA", "CPU", or "MOCK"

# ─── Detect & Initialize ───────────────────────────────────────────
def initialize_engine(model_name: str = "google/gemma-2b"):
    """
    Probes the runtime environment and loads the model on the best 
    available hardware. Called ONCE at server startup.
    
    Priority: TPU (v5e) → NVIDIA GPU (T4) → CPU → Mock (fallback)
    """
    global _engine, _hardware_type

    # ── 1. Try Google TPU via torch_xla ────────────────────────────
    try:
        import torch
        import torch_xla.core.xla_model as xm
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print("🔍 Probing for TPU hardware...")
        device = xm.xla_device()
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model = model.to(device)

        _engine = {"model": model, "tokenizer": tokenizer, "device": device}
        _hardware_type = "TPU"
        print(f"🚀 TPU v5e ACTIVE — Model: {model_name}")
        return

    except Exception as e:
        print(f"⚠️  TPU not available: {e}")

    # ── 2. Try NVIDIA CUDA GPU (T4 / A100 / etc.) ─────────────────
    try:
        import torch
        if torch.cuda.is_available():
            from transformers import AutoModelForCausalLM, AutoTokenizer

            print("🔍 NVIDIA GPU detected, loading model in float16...")
            device = torch.device("cuda")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # float16 is crucial for fitting on a 16GB T4 GPU
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype=torch.float16
            )

            _engine = {"model": model, "tokenizer": tokenizer, "device": device}
            _hardware_type = "CUDA"
            print(f"🎮 NVIDIA GPU ACTIVE — Model: {model_name}, VRAM: {torch.cuda.get_device_name(0)}")
            return

    except Exception as e:
        print(f"⚠️  CUDA GPU not available: {e}")

    # ── 3. CPU Fallback (very slow, but works) ─────────────────────
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        print("🔍 No accelerator found, attempting CPU fallback...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        device = torch.device("cpu")

        _engine = {"model": model, "tokenizer": tokenizer, "device": device}
        _hardware_type = "CPU"
        print(f"🐢 CPU ACTIVE — Model: {model_name} (this will be slow)")
        return

    except Exception as e:
        print(f"⚠️  CPU model load failed: {e}")

    # ── 4. Mock Fallback (no model, simulated output) ──────────────
    _engine = None
    _hardware_type = "MOCK"
    print("🧪 MOCK ENGINE ACTIVE — No model loaded, using simulated responses.")


def get_hardware_type() -> str:
    """Returns the active hardware type string."""
    return _hardware_type


def get_engine():
    """Returns the initialized engine dict (model, tokenizer, device) or None."""
    return _engine


# ─── Synchronous Generation (for legacy agent calls) ──────────────
def generate_response(prompt: str, max_new_tokens: int = 256) -> str:
    """
    Synchronous text generation. Used by all existing agents 
    (briefing, impact, opinions, timeline, debate, etc.)
    """
    global _engine, _hardware_type

    if _hardware_type == "MOCK" or _engine is None:
        return _generate_mock_response(prompt)

    try:
        model = _engine["model"]
        tokenizer = _engine["tokenizer"]
        device = _engine["device"]

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        
        if _hardware_type == "TPU":
            import torch_xla.core.xla_model as xm
            inputs = {k: v.to(device) for k, v in inputs.items()}
        elif _hardware_type == "CUDA":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        # CPU: inputs are already on CPU

        import torch
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )

        # Decode only the generated portion (skip the input tokens)
        generated = outputs[0][inputs["input_ids"].shape[-1]:]
        return tokenizer.decode(generated, skip_special_tokens=True).strip()

    except Exception as e:
        print(f"❌ Generation error on {_hardware_type}: {e}")
        return _generate_mock_response(prompt)


# ─── Async Streaming Generation (for SSE/frontend) ────────────────
async def stream_tokens(prompt: str, max_new_tokens: int = 256):
    """
    Async generator that yields tokens one-by-one for SSE streaming.
    Works on TPU, CUDA, CPU, or falls back to mock simulation.
    """
    global _engine, _hardware_type

    if _hardware_type == "MOCK" or _engine is None:
        async for token in _stream_mock_tokens(prompt):
            yield token
        return

    try:
        model = _engine["model"]
        tokenizer = _engine["tokenizer"]
        device = _engine["device"]

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)

        if _hardware_type in ("TPU", "CUDA"):
            inputs = {k: v.to(device) for k, v in inputs.items()}

        import torch

        # Generate all tokens at once, then stream them to the frontend
        # (True token-by-token generation requires a custom loop; this 
        #  approach gives the same UX with simpler code)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )

        generated = outputs[0][inputs["input_ids"].shape[-1]:]
        full_text = tokenizer.decode(generated, skip_special_tokens=True).strip()

        # Stream word-by-word to simulate real-time generation UX
        words = full_text.split()
        for word in words:
            yield f" {word}"
            await asyncio.sleep(0.03)  # ~33 tokens/sec streaming rate

    except Exception as e:
        print(f"❌ Streaming error on {_hardware_type}: {e}")
        async for token in _stream_mock_tokens(prompt):
            yield token


# ─── Mock Fallback Generators ─────────────────────────────────────
def _generate_mock_response(prompt: str) -> str:
    """Produces a plausible mock response when no model is loaded."""
    return (
        "Based on the JAX/XLA analysis of the current news cluster: "
        "The breakthrough in TPU v5e-1 parallelization allows for real-time clustering. "
        "Key takeaway: Market volatility is high but stable."
    )


async def _stream_mock_tokens(prompt: str):
    """Simulates word-by-word streaming for demo/testing."""
    tokens = [
        " AI-Native", " Market", " Insights:", " The", " current", " cluster", " analysis",
        " indicates", " a", " shift", " in", " high-frequency", " trading.",
        " Analyzing", " sentiment", " across", " top", " sources...",
        " Detected", " bullish", " divergence", " in", " tech", " sector", " news.",
        " Market", " impact", " score", " is", " high", " (8.4/10).",
        " Our", " deep-briefing", " suggests", " the", " story", " arc", " is", " peaking", " today.",
        " Further", " details", " on", " regulatory", " changes", " are", " arriving", " in", " real-time.",
        " Strategic", " recommendation:", " monitor", " the", " sector", " overlap.",
        " End", " of", " dynamic", " briefing."
    ]
    for token in tokens:
        yield token
        await asyncio.sleep(0.04)
