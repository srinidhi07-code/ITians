# main.py
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import IncidentRequest
from agent import run_agent

app = FastAPI(title="Incident Response Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # we will restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Incident Response Agent is running"}

@app.post("/analyze")
def analyze_incident(incident: IncidentRequest):
    for attempt in range(3):
        try:
            result = run_agent(
                incident_id=incident.incident_id,
                title=incident.title,
                description=incident.description,
                severity=incident.severity
            )
            return result
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"[Agent] Rate limited. Waiting 30s before retry {attempt+1}/3...")
                time.sleep(30)
            else:
                raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=429, detail="Rate limit hit. Please wait 1 minute and try again.")

@app.get("/health")
def health():
    return {"status": "ok"}