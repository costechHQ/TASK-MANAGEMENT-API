from fastapi import FastAPI
from database import create_db_and_tables
from fastapi import Depends, FastAPI
from dependencies import require_api_key, PaginationParams

app =  FastAPI(title="Task Management API")


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.get("/")
async def home():
    return {"message": "Task Management API"}

@app.post("/test")
async def test_write_operation(
    api_key: str = Depends(require_api_key)
):
    return {"message": "API key accepted"}

@app.get("/test-pagination")
async def test_pagination(
    pagination: PaginationParams = Depends(PaginationParams)
):
    return {
        "page": pagination.page,
        "limit": pagination.limit,
        "offset": pagination.offset,
    }