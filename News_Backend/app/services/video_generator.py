import os
import json
import requests
import subprocess
import asyncio
import re
from pathlib import Path
from moviepy import ImageSequenceClip, AudioFileClip
import edge_tts
from app.services.llm_service import generate_llm_response
import urllib.parse

def generate_news_short(cluster_text: str, story_id: str) -> str:
    """
    Generate a 30s video short using LLM -> edge-tts -> Pollinations -> moviepy
    Returns the static URL or file path of the generated .mp4.
    """
    out_dir = Path(f"videos/{story_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    mp4_path = out_dir / f"{story_id}_explainer.mp4"
    if mp4_path.exists():
        return f"/videos/{story_id}/{story_id}_explainer.mp4"
    
    # 1. Groq (Llama 3.3) for Script and Prompts
    prompt = f"""
    You are a viral news anchor scriptwriter.
    Read the following news material and write a 30-second spoken summary.
    Also, generate exactly 3 highly descriptive image prompts related to the story to be shown on screen.
    
    Return ONLY a JSON object with this exact structure:
    {{
       "script": "The punchy 30-second script...",
       "image_prompts": ["Prompt 1", "Prompt 2", "Prompt 3"]
    }}
    
    Source Material:
    {cluster_text[:2000]}
    """
    
    script = "Significant developments have occurred in our top story today. Stay tuned for details."
    prompts = ["Breaking news abstract background", "Global digital connectivity network", "Financial market data terminal"]

    try:
        response = generate_llm_response(prompt)
        # Robust JSON extraction
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            script = data.get("script", script)
            prompts = data.get("image_prompts", prompts)
        else:
             print(f"⚠️ Warning: No JSON found in LLM response for story {story_id}. Using fallbacks.")
    except Exception as e:
        print(f"Failed to parse LLM response for video generator: {e}")
        # Not raising, just using fallbacks to prevent 500 error

    # 2. edge-tts (Python API to avoid subprocess issues)
    mp3_path = out_dir / f"{story_id}_voice.mp3"
    
    async def speak():
        communicate = edge_tts.Communicate(script, "en-US-ChristopherNeural")
        await communicate.save(str(mp3_path))
    
    try:
        asyncio.run(speak())
    except Exception as e:
        print(f"❌ edge-tts failed: {e}")
        # Fallback empty audio or similar if needed, but we'll let moviepy handle it
    
    if not mp3_path.exists():
        raise Exception("Audio generation failed.")

    # 3. Pollinations API (Images)
    img_paths = []
    # Ensure we have 3 prompts
    prompts = prompts[:3]
    while len(prompts) < 3:
        prompts.append(f"Abstract digital background {len(prompts)+1}")

    for i, p in enumerate(prompts):
        try:
            encoded_prompt = urllib.parse.quote(p)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={i}"
            r = requests.get(url, timeout=30)
            img_path = out_dir / f"{story_id}_img_{i}.jpg"
            if r.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(r.content)
                img_paths.append(str(img_path))
            else:
                print(f"⚠️ Warning: Pollinations failed for prompt {i}: {r.status_code}")
        except Exception as e:
             print(f"⚠️ Warning: Image fetch error: {e}")
            
    if not img_paths:
        raise Exception("No images could be fetched for the video.")

    # 4. moviepy
    try:
        audio = AudioFileClip(str(mp3_path))
        duration = audio.duration
        
        # Assign equal duration for each image to match audio duration
        img_duration = duration / len(img_paths)
        
        clip = ImageSequenceClip(img_paths, durations=[img_duration]*len(img_paths))
        clip = clip.with_audio(audio)
        
        # Save video
        clip.write_videofile(str(mp4_path), fps=24, codec="libx264", audio_codec="aac")
        
        return f"/videos/{story_id}/{story_id}_explainer.mp4"
    except Exception as e:
        print(f"❌ moviepy assembly failed: {e}")
        raise Exception(f"Video assembly failed: {str(e)}")
