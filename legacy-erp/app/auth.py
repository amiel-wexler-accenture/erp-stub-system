import os
from fastapi import Header, HTTPException
from typing import Optional


async def verify_token(authorization: Optional[str] = Header(None)) -> None:
    expected = os.environ.get("LEGACY_API_TOKEN", "")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.removeprefix("Bearer ")
    if token != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
