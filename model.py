from sqlmodel import Field, SQLModel
from enum import Enum


class UserBase(SQLModel):
    name: str
    email:str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    id: int

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
class TaskBase(SQLModel):
    title: str
    description: str

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: TaskStatus = TaskStatus.TODO
    user_id: int = Field(foreign_key="user.id")
class TaskCreate(TaskBase):
    user_id: int

class TaskPublic(TaskBase):
    id: int
    status: TaskStatus
    user_id: int

class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
