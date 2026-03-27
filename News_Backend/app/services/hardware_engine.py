"""
Hardware Abstraction Layer (HAL) for AI-Native News Experience.
Dynamically detects Gemini API → TPU v5e → NVIDIA GPU → CPU → Mock.
Priority: Gemini API (highest quality) → TPU (fast local) → GPU → CPU → Mock.
"""
import os
import sys
import asyncio
import google.generativeai as genai

# ─── Global State ───────────────────────────────────────────────────
_engine = None          # Will hold the initialized model/tokenizer/device or Gemini client
_hardware_type = "MOCK" # "GEMINI", "TPU", "CUDA", "CPU", or "MOCK"

# ─── Detect & Initialize ───────────────────────────────────────────
def initialize_engine(model_name: str = "google/gemma-2b"):
    """
    Probes the runtime environment and loads the model on the best 
    available hardware. Called ONCE at server startup.
    """
    global _engine, _hardware_type

    # ── 1. Check for Gemini API Key (User Preferred for 'Humanized' data) ──
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            print("💎 Probing for Gemini API...")
            genai.configure(api_key=gemini_key)
            # Use 'gemini-1.5-flash' for speed, or 'gemini-1.5-pro' for depth
            model = genai.GenerativeModel('gemini-1.5-flash')
            _engine = {"model": model}
            _hardware_type = "GEMINI"
            print("🚀 GEMINI API ACTIVE — Quality: Human-Level")
            return
        except Exception as e:
            print(f"⚠️  Gemini init failed: {e}")

    # ── 2. Try Google TPU via torch_xla ────────────────────────────
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

    # ── 3. Try NVIDIA CUDA GPU (T4 / A100 / etc.) ─────────────────
    try:
        import torch
        if torch.cuda.is_available():
            from transformers import AutoModelForCausalLM, AutoTokenizer

            print("🔍 NVIDIA GPU detected, loading model in float16...")
            device = torch.device("cuda")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype=torch.float16
            )

            _engine = {"model": model, "tokenizer": tokenizer, "device": device}
            _hardware_type = "CUDA"
            print(f"🎮 NVIDIA GPU ACTIVE — Model: {model_name}")
            return

    except Exception as e:
        print(f"⚠️  CUDA GPU not available: {e}")

    # ── 4. CPU Fallback (very slow, but works) ─────────────────────
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        print("🔍 No accelerator found, attempting CPU fallback...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        device = torch.device("cpu")

        _engine = {"model": model, "tokenizer": tokenizer, "device": device}
        _hardware_type = "CPU"
        print(f"🐢 CPU ACTIVE — Model: {model_name}")
        return

    except Exception as e:
        print(f"⚠️  CPU model load failed: {e}")

    # ── 5. Mock Fallback (no model, simulated output) ──────────────
    _engine = None
    _hardware_type = "MOCK"
    print("🧪 MOCK ENGINE ACTIVE — No model loaded, using simulated responses.")


def get_hardware_type() -> str:
    """Returns the active hardware type string."""
    return _hardware_type


def get_engine():
    """Returns the initialized engine dict or None."""
    return _engine


# ─── Synchronous Generation (for legacy agent calls) ──────────────
def generate_response(prompt: str, max_new_tokens: int = 256) -> str:
    """
    Synchronous text generation.
    """
    global _engine, _hardware_type

    if _hardware_type == "GEMINI":
        try:
            model = _engine["model"]
            # Humanizing prompt wrapper
            humanized_prompt = f"Humanize this news data and provide a concise briefing:\n{prompt}"
            response = model.generate_content(humanized_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Gemini generation error: {e}")
            return _generate_mock_response(prompt)

    if _hardware_type == "MOCK" or _engine is None:
        return _generate_mock_response(prompt)

    try:
        model = _engine["model"]
        tokenizer = _engine["tokenizer"]
        device = _engine["device"]

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        
        if _hardware_type in ("TPU", "CUDA"):
            inputs = {k: v.to(device) for k, v in inputs.items()}

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

        generated = outputs[0][inputs["input_ids"].shape[-1]:]
        return tokenizer.decode(generated, skip_special_tokens=True).strip()

    except Exception as e:
        print(f"❌ Generation error on {_hardware_type}: {e}")
        return _generate_mock_response(prompt)


# ─── Async Streaming Generation (for SSE/frontend) ────────────────
async def stream_tokens(prompt: str, max_new_tokens: int = 256):
    """
    Async generator that yields tokens one-by-one for SSE streaming.
    """
    global _engine, _hardware_type

    if _hardware_type == "GEMINI":
        try:
            model = _engine["model"]
            humanized_prompt = f"Humanize this news briefing and provide insight:\n{prompt}"
            response = model.generate_content(humanized_prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                await asyncio.sleep(0.01)
            return
        except Exception as e:
            print(f"❌ Gemini streaming error: {e}")
            async for token in _stream_mock_tokens(prompt):
                yield token
            return

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

        words = full_text.split()
        for word in words:
            yield f" {word}"
            await asyncio.sleep(0.03)

    except Exception as e:
        print(f"❌ Streaming error on {_hardware_type}: {e}")
        async for token in _stream_mock_tokens(prompt):
            yield token


# ─── Mock Fallback Generators ─────────────────────────────────────
def _generate_mock_response(prompt: str) -> str:
    return (
        "AI-Native Terminal Hub: Standardizing news story arcs. "
        "The current volatility metrics indicate a stabilization in tech sectors."
    )


async def _stream_mock_tokens(prompt: str):
    tokens = [" Connecting", " to", " AI", " Intelligence", " Core...", " Done.", " Deciphering", " story", " impact."]
    for token in tokens:
        yield token
        await asyncio.sleep(0.04)
