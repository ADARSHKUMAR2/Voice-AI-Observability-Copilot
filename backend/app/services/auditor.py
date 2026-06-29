import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from app.models.call_log import VoiceTranscriptPayload, CallLogDocument
from app.models.audit_result import AuditResult

load_dotenv()

SYSTEM_PROMPT = (
    "You are an expert Voice AI Quality Auditor. Analyze the provided conversation transcript. "
    "Identify script deviations, broken instruction rules, or missed customer retention opportunities."
)

async def audit_voice_transcript(payload: VoiceTranscriptPayload) -> CallLogDocument:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("CRITICAL: GITHUB_TOKEN is missing from your environment variables!")

    model = OpenAIChatModel(
        "gpt-4o",
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

    analysis: AuditResult = result.data

    return CallLogDocument(
        locationId=payload.locationId,
        agentId=payload.agentId,
        callId=payload.callId,
        transcript=payload.transcript,
        status=analysis.status,
        score=analysis.score,
        deviations=analysis.deviations,
        recommendation=analysis.recommendation,
    )