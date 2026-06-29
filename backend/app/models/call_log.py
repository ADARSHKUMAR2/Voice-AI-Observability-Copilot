from typing import Optional
from pydantic import BaseModel
from beanie import Document
from datetime import datetime

class VoiceTranscriptPayload(BaseModel):
    locationId: Optional[str] = None
    agentId: Optional[str] = None
    callId: Optional[str] = None
    transcript: Optional[str] = None

class CallLogDocument(Document):
    locationId: Optional[str] = None
    agentId: Optional[str] = None
    callId: Optional[str] = None
    transcript: Optional[str] = None
    status: str
    score: int
    deviations: list[str]
    recommendation: str
    createdAt: datetime = datetime.utcnow()

    class Settings:
        name = "call_audit_logs"