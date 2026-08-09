from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User

class Books(SQLModel, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: int
    is_sold: bool = Field(default=False)

    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


class BooksCreate(SQLModel):
    title: str
    author: str
    price: int
    user_id: int


class BooksRead(SQLModel):
    id: int 
    title: str
    author: str
    price: int
    is_sold: bool
    user_id: int

Books.model_rebuild()


class BookUpdate(SQLModel):
    price: Optional[int] = None