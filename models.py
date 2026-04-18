# models.py
from pydantic import BaseModel

class IncidentRequest(BaseModel):
    incident_id: str
    title: str
    description: str
    severity: str  # critical, high, medium, low

class AgentResponse(BaseModel):
    incident_id: str
    root_cause: str
    remediation_steps: list[str]
    summary: str