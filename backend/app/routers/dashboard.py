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
    
    # Deduplicate by callId: keep only the most recent entry for each unique callId
    unique_logs = {}
    for log in raw_logs:
        key = log.callId if log.callId else "Sandbox_Simulation"
        # If we haven't seen this callId, or this entry is newer, keep it
        if key not in unique_logs or (log.createdAt and unique_logs[key].createdAt and log.createdAt > unique_logs[key].createdAt):
            unique_logs[key] = log
    
    formatted_data = []
    for log in unique_logs.values():
        
        raw_status = str(log.status).strip().upper()
        normalized_status = "PASS" if raw_status in ["PASS", "SUCCESS", "SUCCESSFUL"] else "FAIL"
        
        formatted_data.append({
            "id": str(log.id),
            "callId": log.callId if log.callId else "Sandbox_Simulation",
            "agentId": log.agentId if log.agentId else "Unassigned_Bot",
            "status": normalized_status,  # 🎯 Injected normalized label contract
            "adherenceScore": getattr(log, "score", 0) if getattr(log, "score", None) is not None else 0, 
            "deviations": log.deviations if log.deviations else [],
            "recommendation": log.recommendation if log.recommendation else "No recommendation available.",
            "transcript": log.transcript
        })
        
    return {"data": formatted_data}
