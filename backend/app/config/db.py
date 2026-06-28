import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
from pymongo.driver_info import DriverInfo

from app.models.agent import AgentProfile
from app.models.evaluation import CallEvaluation
from app.models.action import UseAction

load_dotenv()

# ── Motor 3.7+ compatibility shim ──────────────────────────────────────
# Motor 3.7+ does not forward ``append_metadata`` from pymongo's
# MongoClient to the Motor wrapper.  Because AsyncIOMotorClient.__getattr__
# treats any unknown attribute name as a database reference,
#   client.append_metadata
# returns a MotorDatabase named ``"append_metadata"`` instead of the real
# method.  Beanie 2.1.0 calls this method during ``init_beanie``, so we
# expose it explicitly here to bypass the ``__getattr__`` fallback.
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