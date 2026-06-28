from typing import List, Optional
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field

class KPICheck(BaseModel):
    kpiName: str
    passed: bool
    notes: str

class CallEvaluation(Document):
    agentId: str = Field(..., index=True)
    locationId: str = Field(..., index=True)
    ghlCallId: str = Field(..., unique=True)
    transcript: str
    adherenceScore: float = Field(..., ge=0, le=100)
    hasCriticalFailure: bool = False
    kpiBreakdown: List[KPICheck] = []
    recommendation: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "call_evaluations"