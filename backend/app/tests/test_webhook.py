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