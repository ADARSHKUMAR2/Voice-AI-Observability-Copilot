import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
from pymongo.driver_info import DriverInfo

from app.models.agent import AgentProfile
from app.models.evaluation import CallEvaluation
from app.models.action import UseAction

load_dotenv()

def _motor_append_metadata(
    self: AsyncIOMotorClient, driver_info: DriverInfo
) -> None:
    """Delegate ``append_metadata`` to the underlying pymongo MongoClient."""
    self.delegate.append_metadata(driver_info)


AsyncIOMotorClient.append_metadata = _motor_append_metadata
# ────────────────────────────────────────────────────────────────────────

async def init_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/observability_copilot")
    
    # Create the client
    client = AsyncIOMotorClient(mongo_uri)
    
    # Get the target database name cleanly from the URI, or default it
    database = client.get_default_database()

    # Initialize Beanie using the correct database context
    await init_beanie(
        database=database,
        document_models=[
            AgentProfile,
            CallEvaluation,
            UseAction
        ]
    )
    print("🚀 Asynchronous Beanie ODM pipeline database online.")