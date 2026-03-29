"""
Hardware Abstraction Layer (HAL) for AI-Native News Experience.
Dynamically detects Gemini API → TPU v5e → NVIDIA GPU → CPU → Mock.
Priority: Gemini API (highest quality) → TPU (fast local) → GPU → CPU → Mock.
"""
import os
import sys
import json
import asyncio
import google.generativeai as genai
from groq import Groq

# ─── Global State ───────────────────────────────────────────────────
_engine = None          # Will hold the initialized model/tokenizer/device or Gemini client or Groq
_hardware_type = "MOCK" # "GEMINI", "GROQ", "TPU", "CUDA", "CPU", or "MOCK"

# ─── Detect & Initialize ───────────────────────────────────────────
def initialize_engine(model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    global _engine, _hardware_type

    # ── 1. Check for Gemini API Key (User Preferred for 'Humanized' data) ──
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            print("💎 Probing for Gemini API...")
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Test prompt to ensure key is valid
            model.generate_content("ping")
            _engine = {"model": model}
            _hardware_type = "GEMINI"
            print("🚀 GEMINI API ACTIVE — Quality: Human-Level (Gemini 1.5 Flash)")
            return
        except Exception as e:
            print(f"⚠️  Gemini init failed: {e}")

    # ── 2. Check for Groq API Key (High Speed LPU Inference) ────────────────
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            print("⚡ Probing for Groq LPU...")
            client = Groq(api_key=groq_key)
            # Use Llama-3.3-70b-versatile (Current high-performance versatile model)
            _engine = {"client": client, "model": "llama-3.3-70b-versatile"}
            _hardware_type = "GROQ"
            print("🚀 GROQ LPU ACTIVE — Speed: Ultra-Fast (Llama 3.3)")
            return
        except Exception as e:
            print(f"⚠️  Groq init failed: {e}")

    # ── 2. Try Google TPU via torch_xla ────────────────────────────
    try:
        import torch
        import torch_xla.core.xla_model as xm
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print("🔍 Probing for TPU hardware...")
        device = xm.xla_device()
        print(f"📦 Loading local model {model_name} on TPU...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model = model.to(device)

        _engine = {"model": model, "tokenizer": tokenizer, "device": device}
        _hardware_type = "TPU"
        print(f"🚀 TPU v5e ACTIVE — Model: {model_name}")
        return

    except Exception as e:
        print(f"⚠️  TPU not available or failed: {str(e)[:100]}")

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
        print(f"⚠️  CUDA GPU not available: {str(e)[:100]}")

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
        print(f"⚠️  CPU model load failed: {str(e)[:100]}")

    # ── 5. Mock Fallback (no model, simulated output) ──────────────
    _engine = None
    _hardware_type = "MOCK"
    print("🧪 MOCK ENGINE ACTIVE — No model loaded, using simulated responses.")


def get_hardware_type() -> str:
    return _hardware_type


def get_engine():
    return _engine


# ─── Synchronous Generation (for legacy agent calls) ──────────────
def generate_response(prompt: str, max_new_tokens: int = 256) -> str:
    global _engine, _hardware_type

    if _hardware_type == "GEMINI":
        try:
            model = _engine["model"]
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Gemini generation error: {e}")
            return _generate_mock_response(prompt)

    if _hardware_type == "GROQ":
        try:
            client = _engine["client"]
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=_engine["model"],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Groq generation error: {e}")
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
    global _engine, _hardware_type

    if _hardware_type == "GEMINI":
        try:
            model = _engine["model"]
            response = model.generate_content(prompt, stream=True)
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

    if _hardware_type == "GROQ":
        try:
            client = _engine["client"]
            stream = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=_engine["model"],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                await asyncio.sleep(0.01)
            return
        except Exception as e:
            print(f"❌ Groq streaming error: {e}")
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
    prompt_upper = prompt.upper()
    
    # CASE: JSON output expected (Timeline, Intelligence, etc.)
    if "JSON" in prompt_upper:
        # Detect Timeline prompt
        if "TIMELINE" in prompt_upper or "CHRONOLOGICAL" in prompt_upper:
            return json.dumps({
                "events": [
                    {"date": "2 Days Ago", "event": "Initial market signal detected in Asian sectors."},
                    {"date": "Yesterday", "event": "Major stakeholders confirm strategy pivot."},
                    {"date": "6 Hours Ago", "event": "Public statement released; high volatility observed."},
                    {"date": "Now", "event": "Story reaching peak complexity; analysts evaluating impact."}
                ],
                "sentiment_arc": "The narrative shifted from cautious optimism to high-risk instability as details merged.",
                "predictions": [
                    "Regulators likely to intervene by next fiscal quarter.",
                    "Secondary market ripple effects expected in logistics.",
                    "Consumer confidence may dip temporarily before stabilizing."
                ]
            })
            
        # Detect Dashboard/Intelligence prompt
        return json.dumps({
            "headline": "Aureum Intelligence: System-Wide Narrative Synthesis",
            "summary": "Our neural clusters have identified a stabilizing trend in the current news cycle. Market indicators suggest a 12% rise in sentiment following recent policy adjustments.",
            "why_matters": [
                "Direct impact on Q3 fiscal projections",
                "Shifts standard industry benchmarks for the first time in years",
                "Triggers automated hedging protocols across several sectors"
            ],
            "sentiment": "NEUTRAL-BULLISH",
            "sectors": ["Global Logistics", "Fintech Architecture", "Renewable Energy"],
            "radar": { "bullish": 0.75, "bearish": 0.15, "interest": 0.95 }
        })
    
    # CASE: Plain text output expected (Opinions, Chat, etc.)
    
    # Detect Contrarian Opinions
    if "CONTRAST" in prompt_upper or "OPPOSING" in prompt_upper or "VIEWPOINT" in prompt_upper:
        return """Viewpoint A: The bull case suggests that the recent technological integration will lead to unprecedented efficiency and market dominance.

Viewpoint B: However, skeptics argue that the high cost of implementation and potential regulatory hurdles pose significant risks to long-term stability."""

    # Default Chat/Narration
    return "Aureum Signal: The story arc is currently expanding. We are tracking a 14% increase in narrative momentum centered around strategic shifts in the sector. Further intelligence is being synthesized by our JAX-TPU clusters."


async def _stream_mock_tokens(prompt: str):
    # Detect if we should stream JSON or text
    if "JSON" in prompt:
        text = _generate_mock_response(prompt)
        words = text.split()
        for word in words:
            yield f" {word}"
            await asyncio.sleep(0.02)
    else:
        tokens = [" Connecting", " to", " AI", " Intelligence", " Core...", " Done.", " Deciphering", " story", " impact."]
        for token in tokens:
            yield token
            await asyncio.sleep(0.04)
