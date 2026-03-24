import sys
import os

# Add the project root to sys.path
sys.path.append(r"c:\dev\AI-Native News Experience\News_Backend")

try:
    from app.agents.story_agent import get_all_stories
    print("Import successful")
    stories = get_all_stories()
    print(f"Stories: {stories}")
except Exception as e:
    import traceback
    traceback.print_exc()
