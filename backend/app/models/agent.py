from typing import List, Dict
from beanie import Document
from pydantic import BaseModel, Field

class KPIItem(BaseModel):
    name: str
    description: str

class AgentProfile(Document):
    locationId: str = Field(..., index=True)
    agentId: str = Field(..., unique=True)
    agentName: str
    systemPrompt: str
    kpis: List[KPIItem] = []

    class Settings:
        name = "agent_profiles"