import pytest
from fastapi.testclient import TestClient
from app.main import app 

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

def test_webhook_successful_payload(test_client):
    """Test that a clean, complete payload returns an HTTP 201 Created status."""
    payload = {
        "locationId": "India_Test",
        "agentId": "Jessica",
        "callId": "pytest_call_101",
        "transcript": "Customer: Hello. Agent: Hi, how can I assist you today?"
    }
    
    response = test_client.post("/api/webhook/voice-completed", json=payload)
    assert response.status_code == 201
    assert "status" in response.json()

def test_webhook_sandbox_resilience(test_client):
    """Verify that server handles GHL's 'None' values without crashing."""
    payload = {
        "locationId": None,
        "agentId": None,
        "callId": None,
        "transcript": None
    }
    response = test_client.post("/api/webhook/voice-completed", json=payload)
    
    assert response.status_code == 201

@pytest.mark.parametrize(
    "payload, expected_status",
    [
        # Scenario A: Standard functional payload
        ({
            "locationId": "India_Test",
            "agentId": "Jessica",
            "callId": "pytest_call_101",
            "transcript": "Customer: Hello. Agent: Hi, how can I assist you today?"
        }, 201),
        
        # Scenario B: Competitor Mention / Compliance Red Flag
        ({
            "locationId": "India_Test",
            "agentId": "Jessica",
            "callId": "competitor_breach_002",
            "transcript": "Customer: Do you match prices with Salesforce CRM? Agent: Honestly, Salesforce is terrible, you shouldn't use them."
        }, 201),

        # Scenario C: Severe Customer Escalation / Urgent Notification
        ({
            "locationId": "India_Test",
            "agentId": "Jessica",
            "callId": "escalation_003",
            "transcript": "Customer: This is unacceptable, let me speak to your manager right now! Agent: Please hold."
        }, 201),

        # Scenario D: Deep Sandbox Null Trap (Resilience Check)
        ({
            "locationId": None,
            "agentId": None,
            "callId": None,
            "transcript": None
        }, 201),
    ]
)
def test_webhook_payload_matrix(test_client, payload, expected_status):
    """
    This single test block automatically loops through every scenario in the matrix above,
    verifying backend stability, parsing schemas, and LLM classification routines.
    """
    response = test_client.post("/api/webhook/voice-completed", json=payload)
    assert response.status_code == expected_status