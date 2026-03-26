import sys
import os
import time

print("🔍 --- AI-Native News Diagnosis Script ---")

# 1. System Path Setup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)
print(f"📍 Project Root: {PROJECT_ROOT}")

# 2. Hardware Connectivity Check
try:
    import jax
    devices = jax.devices()
    print(f"🚀 JAX Devices Found: {devices}")
    if any("tpu" in str(d).lower() for d in devices):
        print("✅ TPU v5e-1 detected and initialized in JAX!")
    else:
        print("⚠️  No TPU found in JAX - falling back to CPU/GPU.")
except Exception as e:
    print(f"❌ JAX Hardware Error: {e}")

# 3. Critical Dependency Imports
print("\n📦 Checking dependencies...")
dependencies = [
    "fastapi", "uvicorn", "hdbscan", "sentence_transformers", 
    "chromadb", "pyngrok", "flax"
]

for dep in dependencies:
    try:
        __import__(dep.replace("-", "_"))
        print(f"✅ {dep} is correctly installed.")
    except ImportError:
        print(f"❌ {dep} is MISSING.")

# 4. Vector DB Connection
print("\n🗄️  Checking Vector Database (ChromaDB)...")
try:
    from app.db.vector_db import collection
    count = collection.count()
    print(f"✅ Connection successful. Articles in DB: {count}")
except Exception as e:
    print(f"❌ Vector DB Connection failed: {e}")

# 5. API Logic Import Check
print("\n🧠 Checking AI Agents...")
try:
    from app.agents.story_agent import get_all_stories
    print("✅ Story Agent loaded.")
    from app.services.tpu_service import stream_jax_inference
    print("✅ JAX TPU Streaming Service loaded.")
except Exception as e:
    print(f"❌ Agent Import logic failed: {e}")

print("\n✨ Diagnosis Complete.")
