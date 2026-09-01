from fastapi import FastAPI, Request
from app.api import conversation, snapshots
from app.config import settings
from app.database import init_db

app = FastAPI(title=settings.app_name, debug=settings.app_debug, 
               description="AI-Powered Stock Market Analyzer API",
               version="1.0.0")

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}


app.include_router(conversation.router, prefix=settings.api_v1_prefix)
app.include_router(snapshots.router, prefix=settings.api_v1_prefix)