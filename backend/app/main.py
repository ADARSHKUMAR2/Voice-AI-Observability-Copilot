from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.db import init_db
from app.routers import webhook, analytics, auth, dashboard
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.call_log import CallLogDocument

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Beanie ODM with Motor MongoDB client on startup
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/voice_copilot")
    client = AsyncIOMotorClient(mongo_uri)
    await init_beanie(database=client.get_default_database(), document_models=[CallLogDocument])
    yield
    # Cleanup operations can go here on shutdown

app = FastAPI(title="Voice AI Observability Copilot", lifespan=lifespan)

class HealthResponse(BaseModel):
    status: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(dashboard.router)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(webhook.router, prefix="/api/webhook", tags=["Ingestion"])

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")