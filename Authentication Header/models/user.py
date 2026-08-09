from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from models.books import Books


class User(SQLModel, table=True):

    id: Optional[int] = Field(None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str

    books: list["Books"] = Relationship(back_populates='owner')

class UserCreate(SQLModel):
    name: str
    email: str
    college: str


class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str

User.model_rebuild()
