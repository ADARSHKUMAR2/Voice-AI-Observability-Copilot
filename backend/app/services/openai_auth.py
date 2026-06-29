import os
import json
from typing import List, Optional
from pydantic import BaseModel
from azure.ai.inference.aio import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

class KPIMatch(BaseModel):
    kpiName: str
    passed: bool
    notes: str

class FlaggedSegment(BaseModel):
    segmentText: str
    reasonForFailure: str

class AuditOutputSchema(BaseModel):
    adherenceScore: float
    hasCriticalFailure: bool
    kpiBreakdown: List[KPIMatch]
    recommendation: str
    flaggedSegments: Optional[List[FlaggedSegment]] = None

async def audit_transcript(transcript: str, system_prompt: str, kpis: list) -> AuditOutputSchema:
    # 1. Initialize the async GitHub Models engine client
    token = os.getenv("GITHUB_TOKEN")
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(token)
    )
    
    # Format incoming KPIs safely as requested by your original schema design
    kpis_formatted = [{"name": k.name, "description": k.description} for k in kpis]

    # 2. Extract the Pydantic schema dynamically to pass as a blueprint
    schema_blueprint = json.dumps(AuditOutputSchema.model_json_schema())

    system_instruction = (
        "You are an enterprise AI Voice Agent Auditor. Analyze the transcription context against the prompt constraints and targeted KPIs.\n"
        "CRITICAL: You MUST output your entire analysis as a single valid JSON object that matches this JSON schema exactly:\n"
        f"{schema_blueprint}"
    )

    # 3. Execute the asynchronous model inference call
    response = await client.complete(
        model="gpt-4o",  
        messages=[
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": f"Voice Agent Prompt: {system_prompt}\nTarget KPIs: {json.dumps(kpis_formatted)}\n\nTranscript:\n{transcript}"
            }
        ],
        temperature=0.2
    )
    
    # 4. Extract and process the generated response payload strings cleanly
    raw_json_content = response.choices[0].message.content
    
    # Close client session resource cleanly
    await client.close()
    
    # 5. Parse and validate the raw text data straight back into your structured Pydantic class object
    return AuditOutputSchema.model_validate_json(raw_json_content)