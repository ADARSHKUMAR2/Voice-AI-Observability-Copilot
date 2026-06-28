from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.models.evaluation import CallEvaluation
from app.models.action import UseAction, ActionStatus

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview")
async def get_location_overview(locationId: str = Query(...)):
    try:
        evaluations = await CallEvaluation.find(CallEvaluation.locationId == locationId).sort("-createdAt").limit(50).to_list()
        actions_queue = await UseAction.find(UseAction.locationId == locationId, UseAction.status == ActionStatus.PENDING).fetch_links().to_list()

        total_calls = len(evaluations)
        avg_adherence = sum(e.adherenceScore for e in evaluations) / total_calls if total_calls > 0 else 0.0
        failures = sum(1 for e in evaluations if e.hasCriticalFailure)

        return {
            "metrics": {
                "totalAuditedCalls": total_calls,
                "averageAdherence": round(avg_adherence, 2),
                "criticalFailureCount": failures,
                "pendingHumanReviews": len(actions_queue)
            },
            "recentEvaluations": evaluations,
            "actionsQueue": actions_queue
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))