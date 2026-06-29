from pydantic import BaseModel


class AuditResult(BaseModel):
    """Structured output model for the voice transcript audit."""
    status: str  # "Pass" or "Fail"
    score: int
    deviations: list[str]
    recommendation: str