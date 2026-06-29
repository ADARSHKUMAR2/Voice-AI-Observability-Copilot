from fastapi import FastAPI
from app.config.db import init_db
from app.routers import webhook, analytics, auth, dashboard
from app.middleware.auth import setup_cors_middleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.call_log import CallLogDocument

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/voice_copilot")
    client = AsyncIOMotorClient(mongo_uri)
    await init_beanie(database=client.get_default_database(), document_models=[CallLogDocument])
    yield

app = FastAPI(title="Voice AI Observability Copilot", lifespan=lifespan)

app.include_router(dashboard.router)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(webhook.router, prefix="/api/webhook", tags=["Ingestion"])

@app.on_event("startup")
async def startup_event():
    await init_db()

setup_cors_middleware(app)

class HealthResponse(BaseModel):
    status: str

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")