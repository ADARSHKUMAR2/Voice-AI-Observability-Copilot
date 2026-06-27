import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

# Load models safely to avoid circular dependencies during registration
from app.models.agent import AgentProfile
from app.models.evaluation import CallEvaluation
from app.models.action import UseAction

load_dotenv()

async def init_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/observability_copilot")
    client = AsyncIOMotorClient(mongo_uri)
    
    # Initialize Beanie with our document models
    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            AgentProfile,
            CallEvaluation,
            UseAction
        ]
    )
    print("🚀 Asynchronous Beanie ODM pipeline database online.")