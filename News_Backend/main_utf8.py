from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.news_api import app as news_app

# Use the pre-configured news_app which already has CORS and all routes
app = news_app

# In case they want to still use the simple main_utf8.py but have it work correctly:
@app.get("/")
def home():
    return {"message": "AI Native News API is active"}
