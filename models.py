# models.py
from pydantic import BaseModel
from typing import List

class IncidentRequest(BaseModel):
    incident_id: str
    title: str
    description: str
    severity: str

class AgentResponse(BaseModel):
    incident_id: str
    analysis: str