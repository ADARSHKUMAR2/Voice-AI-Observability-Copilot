import json
import os
from fastapi import APIRouter, responses
from app.models.call_log import CallLogDocument
from typing import List

router = APIRouter()

@router.get("/dashboard", response_class=responses.HTMLResponse)
async def serve_dashboard():
    """Serve the standalone frontend HTML file."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "index.html")
    with open(frontend_path, "r") as f:
        return f.read()

@router.get("/api/dashboard/data")
async def get_dashboard_data():
    """API endpoint that returns call log data as JSON for the frontend."""
    raw_logs = await CallLogDocument.find_all().to_list()
    return {
        "data": [
            {
                "id": str(log.id),
                "callId": log.callId,
                "agentId": log.agentId,
                "status": log.status,
                "adherenceScore": getattr(log, "score", 0) if getattr(log, "score", None) is not None else 0, 
                "deviations": log.deviations if log.deviations else [],
                "recommendation": log.recommendation if log.recommendation else "No recommendation available.",
                "transcript": log.transcript
            } for log in raw_logs
        ]
    }