from fastapi import Header, HTTPException
from .config import settings

def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if x_api_key != settings.agent_api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return "user_" + x_api_key[:5]  # Simulate a user ID
