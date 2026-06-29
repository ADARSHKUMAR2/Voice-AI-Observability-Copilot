import json
import os
from fastapi import APIRouter, responses
from app.models.call_log import CallLogDocument

router = APIRouter()

@router.get("/dashboard", response_class=responses.HTMLResponse)
async def serve_dashboard():
    """Serve the standalone frontend HTML file."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "index.html")
    with open(frontend_path, "r") as f:
        return f.read()

@router.get("/dashboard/data")
async def get_dashboard_data():
    """API endpoint that returns call log data as JSON for the frontend."""
    raw_logs = await CallLogDocument.find_all().to_list()
    return [
        {
            "id": log.callId,
            "agent": log.agentId,
            "status": log.status,
            "score": log.score,
            "deviations": log.deviations,
            "recommendation": log.recommendation,
            "transcript": log.transcript
        } for log in raw_logs
    ]
