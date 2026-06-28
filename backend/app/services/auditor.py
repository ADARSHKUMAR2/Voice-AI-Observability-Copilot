import os
import json
from dotenv import load_dotenv
from azure.ai.inference.aio import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from app.models.call_log import VoiceTranscriptPayload, CallLogDocument

load_dotenv()

async def audit_voice_transcript(payload: VoiceTranscriptPayload) -> CallLogDocument:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("CRITICAL: GITHUB_TOKEN is missing from your environment variables!")

    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(token)
    )
    
    system_instruction = (
        "You are an expert Voice AI Quality Auditor. Analyze the provided conversation transcript. "
        "Identify script deviations, broken instruction rules, or missed customer retention opportunities. "
        "You MUST return your absolute entire response as a single valid JSON object matching this schema precisely:\n"
        '{"status": "Pass" or "Fail", "score": int, "deviations": ["string"], "recommendation": "string"}\n'
        "Do not include any chat introductory prose. Output raw unformatted text JSON only."
    )
    
    response = await client.complete(
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Transcript: {payload.transcript}"}
        ],
        model="gpt-4o",
        temperature=0.2
    )
    
    # Extract response string and strip leading/trailing whitespace
    raw_content = response.choices[0].message.content.strip()
    
    # 🛡️ DEFENSIVE GUARD: Strip markdown code block wrapping if present
    if raw_content.startswith("```"):
        lines = raw_content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        raw_content = "\n".join(lines).strip()
    
    # Safely unpack the sanitized string token into a structured dictionary
    analysis = json.loads(raw_content)
    
    await client.close()
    
    return CallLogDocument(
        locationId=payload.locationId,
        agentId=payload.agentId,
        callId=payload.callId,
        transcript=payload.transcript,
        status=analysis.get("status", "Fail"),
        score=analysis.get("score", 0),
        deviations=analysis.get("deviations", []),
        recommendation=analysis.get("recommendation", "Review prompt adjustments required.")
    )