from fastapi import APIRouter, HTTPException, status
from app.models.call_log import VoiceTranscriptPayload
from app.services.auditor import audit_voice_transcript


router = APIRouter()

@router.post("/voice-completed", status_code=status.HTTP_201_CREATED)
async def handle_incoming_ghl_transcript(payload: VoiceTranscriptPayload):
    print("\n🚨 DEBUG: INBOUND PAYLOAD RECEIVED FROM GHL:")
    print(payload.model_dump())
    print("🚨 END DEBUG\n")
    
    audit_record = await audit_voice_transcript(payload)
    # await audit_record.insert()
    return {
        "status": "processed", 
        "record_id": audit_record.get("document_id"),
        "audited_by": audit_record.get("audited_by", "Emergency Fallback Node")
    }