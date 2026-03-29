import os
import json
import requests
import subprocess
from pathlib import Path
from moviepy import ImageSequenceClip, AudioFileClip
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
    Read the following news cluster and write a 30-second spoken summary.
    Also, generate exactly 3 highly descriptive image prompts related to the story to be shown on screen.
    
    Return ONLY a JSON object with this exact structure:
    {{
       "script": "The punchy 30-second script...",
       "image_prompts": ["Prompt 1", "Prompt 2", "Prompt 3"]
    }}
    
    News Cluster:
    {cluster_text[:2000]}
    """
    
    try:
        response = generate_llm_response(prompt)
        clean_res = response.strip()
        if "```json" in clean_res:
             clean_res = clean_res.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_res:
             clean_res = clean_res.split("```")[1].strip()
             
        data = json.loads(clean_res)
    except Exception as e:
        print(f"Failed to parse LLM response for video generator: {e}")
        raise ValueError("LLM returned malformed JSON.")
        
    script = data.get("script", "Breaking news: significant developments have occurred in our top story today. Stay tuned for details.")
    prompts = data.get("image_prompts", [])[:3]
    if not isinstance(prompts, list):
        prompts = ["News report abstract background"] * 3
        
    while len(prompts) < 3:
        prompts.append(f"Editorial illustration of the news {len(prompts)+1}")
        
    # 2. edge-tts
    mp3_path = out_dir / f"{story_id}_voice.mp3"
    script_file = out_dir / f"{story_id}_script.txt"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script)
        
    cmd = ["edge-tts", "--voice", "en-US-ChristopherNeural", "-f", str(script_file), "--write-media", str(mp3_path)]
    subprocess.run(cmd, check=True)
    
    # 3. Pollinations API (Images)
    img_paths = []
    for i, p in enumerate(prompts):
        encoded_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
        r = requests.get(url)
        img_path = out_dir / f"{story_id}_img_{i}.jpg"
        if r.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(r.content)
            img_paths.append(str(img_path))
        else:
            raise Exception("Failed to fetch image from Pollinations API.")
            
    # 4. moviepy
    audio = AudioFileClip(str(mp3_path))
    duration = audio.duration
    
    # Assign equal duration for each image to match audio duration
    img_duration = duration / len(img_paths)
    
    clip = ImageSequenceClip(img_paths, durations=[img_duration]*len(img_paths))
    clip = clip.with_audio(audio)
    
    # Needs fps when saving, use 24fps
    clip.write_videofile(str(mp4_path), fps=24, codec="libx264", audio_codec="aac")
    
    return f"/videos/{story_id}/{story_id}_explainer.mp4"
