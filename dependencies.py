from fastapi import Header, HTTPException
from typing import Annotated


API_KEY = "task-secret-123"

def require_api_key(
        api_key: Annotated[str | None, Header(alias="X-API-Key")] = None
):

    if api_key != API_KEY:
        raise HTTPException(
        status_code=401,
        detail="Invalid or missing API key"
    )
    return api_key