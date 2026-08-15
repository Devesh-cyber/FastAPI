from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    '''
    User Model
    '''

    id: Optional[int] = Field(None, primary_key=True)
    name: str = Field(min_length=1, index=True)
    email: str = Field(min_length=1, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)


class UserCreate(SQLModel):
    '''
    Create User Model
    '''

    name: str = Field(min_length=1)
    email: str


class UserRead(SQLModel):
    '''
    Read User Model
    '''

    id: int
    name: str
    email: str
    created_at: datetime