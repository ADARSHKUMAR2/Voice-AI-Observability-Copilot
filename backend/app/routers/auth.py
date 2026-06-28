from fastapi import APIRouter, Header, HTTPException, status

router = APIRouter()

# In production, check this value against an entry in your database
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
        # HighLevel expects a 200, 201, 202, or 204 status code to confirm success
        return {"status": "authenticated", "message": "App connection authorized."}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid authentication token provided."
    )