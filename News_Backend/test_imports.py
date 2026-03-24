import sys
import os

sys.path.append(r"c:\dev\AI-Native News Experience\News_Backend")

agents_dir = r"c:\dev\AI-Native News Experience\News_Backend\app\agents"
for f in os.listdir(agents_dir):
    if f.endswith(".py") and f != "__init__.py":
        mod_name = f"app.agents.{f[:-3]}"
        try:
            __import__(mod_name)
            print(f"Import {mod_name} OK")
        except ModuleNotFoundError as e:
            print(f"Import {mod_name} FAILED: {e}")
        except Exception as e:
            print(f"Import {mod_name} EXCEPTION: {e}")
