from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from dependencies import require_api_key, PaginationParams
from model import User, UserCreate, UserPublic

app =  FastAPI(title="Task Management API")


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.get("/")
async def home():
    return {"message": "Task Management API"}

@app.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED,)
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(require_api_key),
):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[UserPublic])
def get_users(
    session: Session = Depends(get_session),
    pagination: PaginationParams = Depends(PaginationParams),
):
    statement = (
        select(User)
        .offset(pagination.offset)
        .limit(pagination.limit)
    )
    users = session.exec(statement).all()
    return users

