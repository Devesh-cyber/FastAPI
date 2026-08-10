from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.issues import Issues


class Citizens(SQLModel, table=True):
    __tablename__ = "citizens"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    name: str = Field(
        max_length=50,
        index=True
    )

    contact_no: str = Field(
        min_length=10,
        max_length=10,
        regex=r"^\d{10}$",
        description="Mobile number must contain exactly 10 digits"
    )

    locality: str = Field(
        max_length=100,
        index=True
    )

    issues: list["Issues"] = Relationship(
        back_populates="citizen"
    )


class CreateCitizens(SQLModel):
    name: str = Field(max_length=50)

    contact_no: str = Field(
        min_length=10,
        max_length=10,
        regex=r"^\d{10}$"
    )

    locality: str = Field(max_length=100)


class ReadCitizens(SQLModel):
    id: int
    name: str
    contact_no: str
    locality: str


class UpdateCitizens(SQLModel):
    name: Optional[str] = Field(
        default=None,
        max_length=50
    )

    contact_no: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=10,
        regex=r"^\d{10}$"
    )

    locality: Optional[str] = Field(
        default=None,
        max_length=100
    )