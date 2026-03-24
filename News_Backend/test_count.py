import sys
import os

sys.path.append(r"c:\dev\AI-Native News Experience\News_Backend")

try:
    from app.db.vector_db import collection
    count = collection.count()
    print(f"Collection count: {count}")
except Exception as e:
    import traceback
    traceback.print_exc()
