from fastapi import FastAPI
from database import create_db_and_tables

app =  FastAPI(title="Task Management API")


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.get("/")
async def home():
    return {"message": "Task Management API"}