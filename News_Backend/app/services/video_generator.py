import os
import json
import requests
import subprocess
import asyncio
import re
import time
from pathlib import Path
from moviepy import ImageSequenceClip, AudioFileClip, ColorClip, CompositeVideoClip
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
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            script = data.get("script", script)
            prompts = data.get("image_prompts", prompts)
        else:
             print(f"⚠️ Warning: No JSON found in LLM response for story {story_id}. Using fallbacks.")
    except Exception as e:
        print(f"Failed to parse LLM response for video generator: {e}")

    # 2. edge-tts
    mp3_path = out_dir / f"{story_id}_voice.mp3"
    
    async def speak():
        communicate = edge_tts.Communicate(script, "en-US-ChristopherNeural")
        await communicate.save(str(mp3_path))
    
    try:
        if not mp3_path.exists():
            asyncio.run(speak())
    except Exception as e:
        print(f"❌ edge-tts failed: {e}")
    
    if not mp3_path.exists():
        # Create a silent audio or fail gracefully
        raise Exception("Audio generation failed and no fallback available.")

    # 3. Pollinations API (Images) with Resilient Fallbacks
    img_paths = []
    # Ensure we have 3 prompts
    prompts = prompts[:3]
    while len(prompts) < 3:
        prompts.append(f"Abstract digital background {len(prompts)+1}")

    for i, p in enumerate(prompts):
        img_path = out_dir / f"{story_id}_img_{i}.jpg"
        if img_path.exists():
            img_paths.append(str(img_path))
            continue

        success = False
        # Try Pollinations with Retry
        for attempt in range(2):
            try:
                encoded_prompt = urllib.parse.quote(p)
                url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={story_id}{i}"
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(r.content)
                    img_paths.append(str(img_path))
                    success = True
                    break
                else:
                    print(f"⚠️ Pollinations attempt {attempt+1} failed ({r.status_code})")
                    time.sleep(1)
            except Exception as e:
                 print(f"⚠️ Pollinations error: {e}")
                 time.sleep(1)
        
        if not success:
            # Fallback to a reliable placeholder service if Pollinations is down
            try:
                placeholder_url = f"https://picsum.photos/seed/{story_id}{i}/1280/720"
                r = requests.get(placeholder_url, timeout=10)
                if r.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(r.content)
                    img_paths.append(str(img_path))
                    print(f"✅ Used Picsum placeholder for image {i}")
                    success = True
            except:
                pass
            
    # 4. moviepy Assembly with Color Fallback
    try:
        audio = AudioFileClip(str(mp3_path))
        duration = audio.duration
        
        if img_paths:
            # We have at least some images
            img_duration = duration / len(img_paths)
            clip = ImageSequenceClip(img_paths, durations=[img_duration]*len(img_paths))
        else:
            # NO images could be fetched (total API blackout) -> Use a stylized color background
            print("⚠️ Total image failure. Using solid background fallback.")
            clip = ColorClip(size=(1280, 720), color=(20, 20, 40), duration=duration)
            
        clip = clip.with_audio(audio)
        
        # Save video
        clip.write_videofile(str(mp4_path), fps=24, codec="libx264", audio_codec="aac")
        
        return f"/videos/{story_id}/{story_id}_explainer.mp4"
    except Exception as e:
        print(f"❌ moviepy assembly failed: {e}")
        # Last resort: if it fails, don't return 500 if we can help it, but assembly failure is critical
        raise Exception(f"Video assembly failed: {str(e)}")
