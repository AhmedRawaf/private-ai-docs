from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, documents, chat
from app.core.config import get_settings


settings = get_settings()

os.makedirs(os.path.join("data", "indexes"), exist_ok=True)
os.makedirs(os.path.join("data", "storage"), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("private-ai-docs")

app = FastAPI(
    title="Private AI Docs - RAG API",
    version="0.1.0",
    description="Saudi-focused Arabic/English 'Chat with your documents' RAG backend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Application startup complete.")

