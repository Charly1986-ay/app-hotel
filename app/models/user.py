from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str = Field(default=None)
    hashed_password: str


class UserCreate(SQLModel):
    email: str
    full_name: str = None
    password: str


class UserRead(SQLModel):
    id: int
    email: str
    full_name: str
    model_config = {"from_attributes": True}