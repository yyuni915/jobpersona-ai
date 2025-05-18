# backend/app/utils/auth.py

from fastapi import Header, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

def verify_google_token(token: str) -> dict:
    return id_token.verify_oauth2_token(token, google_requests.Request())

async def get_user_id_from_token(
    authorization: str = Header(None)
) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    try:
        token = authorization.split(" ")[1]
        user = verify_google_token(token)
        return user["sub"] 
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
