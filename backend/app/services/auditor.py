import os
import logging
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.models.call_log import VoiceTranscriptPayload, CallLogDocument
from app.models.audit_result import AuditResult

load_dotenv()
logger = logging.getLogger("uvicorn.error")

SYSTEM_PROMPT = (
    "You are an expert Voice AI Quality Auditor. Analyze the provided conversation transcript.\n"
    "Identify script deviations, broken instruction rules, or missed customer retention opportunities."
)

async def audit_voice_transcript(payload: VoiceTranscriptPayload) -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("CRITICAL: GITHUB_TOKEN is missing!")

    MODEL_POOL = [
        "gpt-4o",
        "gpt-4o-mini",
        "Llama-3.3-70B-Instruct",  
        "Mistral-large-2407"       
    ]
    analysis = None
    successfully_audited = False

    for model_name in MODEL_POOL:
        try:
            logger.info(f"📡 Attempting compliance audit using model: {model_name}")
            
            model = OpenAIChatModel(
                model_name,
                provider=OpenAIProvider(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=token,
                ),
            )

            agent = Agent(
                model,
                system_prompt=SYSTEM_PROMPT,
                output_type=AuditResult,
            )

            result = await agent.run(f"Transcript: {payload.transcript}")
            analysis = result.output
            successfully_audited = True
            logger.info(f"✅ Success! Audit completed cleanly via: {model_name}")
            break # Exit the loop immediately upon successful generation

        except Exception as model_err:
            logger.warning(f"⚠️ Model {model_name} rate-limited or unavailable. Swapping to fallback node. Details: {str(model_err)}")
            continue 

    if not successfully_audited or not analysis:
        logger.critical("❌ All models in the pool have exhausted their active execution quotas. Running emergency fallback payload.")
        analysis = AuditResult(
            status="Fail",
            score=0,
            deviations=["Observability pipeline models are currently saturated or rate-limited."],
            recommendation="System is operating under rate restrictions. Re-run test suite later to verify prompt behaviors."
        )

    try:
        audit_record = CallLogDocument(
            locationId=payload.locationId if payload.locationId else "Sandbox",
            agentId=payload.agentId if payload.agentId else "Bot",
            callId=payload.callId,
            transcript=payload.transcript,
            status=analysis.status,
            score=analysis.score,
            deviations=analysis.deviations if analysis.deviations else [],
            recommendation=analysis.recommendation,
        )
        
        await audit_record.insert()
        
        
        return {
            "status": "success",
            "document_id": str(audit_record.id),
            "callId": audit_record.callId
        }
        
    except Exception as db_err:
        logger.error(f"❌ Database Insertion Crash: {str(db_err)}")
        
        return {
            "status": "error",
            "message": f"Database write aborted: {str(db_err)}"
        }