from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from dependencies import require_api_key, PaginationParams
from model import User, UserCreate, UserPublic, Task, TaskCreate, TaskPublic, TaskUpdate




app =  FastAPI(title="Task Management API")


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

@app.get("/")
async def home():
    return {"message": "Task Management API"}

@app.post(
    "/tasks",
    response_model=TaskPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(require_api_key),
):
    user = session.get(User, task.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    db_task = Task.model_validate(task)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

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

@app.get("/tasks", response_model=list[TaskPublic])
async def get_tasks(
    session: Session = Depends(get_session),
    pagination: PaginationParams = Depends(PaginationParams),
):
    statement = (
        select(Task)
        .offset(pagination.offset)
        .limit(pagination.limit)
    )

    tasks = session.exec(statement).all()

    return tasks

@app.put("/tasks/{task_id}", response_model=TaskPublic)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(require_api_key)
):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    task_data = task_update.model_dump(exclude_unset=True)

    for key, value in task_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(require_api_key),
):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    session.delete(task)
    session.commit()