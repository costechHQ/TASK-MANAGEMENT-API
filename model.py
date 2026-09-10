from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str
    email:str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    id: int

class TaskBase(SQLModel):
    title: str
    description: str

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = "todo"
    user_id: int = Field(foreign_key="user,id")


class TaskCreate(TaskBase):
    user_id: int

class TaskPublic(TaskBase):
    id: int
    status: str
    user_id: int