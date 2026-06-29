from fastapi import APIRouter, Header, HTTPException, status

router = APIRouter()

MOCK_VALID_API_KEY = "copilot_secret_test_key_123"

@router.post("/verify")
async def verify_external_user(x_copilot_key: str = Header(None, alias="X-Copilot-Key")):
    if not x_copilot_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Missing secure identification header."
        )
    
    # Simple validation rule check
    if x_copilot_key == MOCK_VALID_API_KEY:
        return {"status": "authenticated", "message": "App connection authorized."}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid authentication token provided."
    )