from fastapi import Header, HTTPException, Query
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

class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
    ):
        self.page = page
        self.limit = limit

    @property
    def offset(self):
        return (self.page - 1) * self.limit