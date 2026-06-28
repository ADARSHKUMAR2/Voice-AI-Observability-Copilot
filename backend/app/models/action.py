from datetime import datetime
from enum import Enum
from beanie import Document, Link
from pydantic import Field
from app.models.evaluation import CallEvaluation

class ActionStatus(str, Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    TRAINED = "TRAINED"

class UseAction(Document):
    callEvaluationId: Link[CallEvaluation]
    locationId: str = Field(..., index=True)
    flaggedSegment: str
    failureReason: str
    status: ActionStatus = ActionStatus.PENDING
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "use_actions"