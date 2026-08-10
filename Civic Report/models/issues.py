from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.citizen import Citizens


class Status(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class Category(str, Enum):
    GARBAGE = "garbage"
    WATER = "water"
    POTHOLE = "pothole"
    STREETLIGHT = "streetlight"
    DRAINAGE = "drainage"
    ROAD_DAMAGE = "road_damage"
    SEWAGE = "sewage"
    PUBLIC_SAFETY = "public_safety"
    OTHER = "other"


class Issues(SQLModel, table=True):
    __tablename__ = "issues"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    category: Category

    # Stores the image path after upload
    image_path: Optional[str] = Field(
        default=None,
        max_length=500
    )

    location: str = Field(
        max_length=150,
        index=True
    )

    description: str = Field(
        max_length=1000
    )

    status: Status = Field(
        default=Status.OPEN
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    citizen_id: int = Field(
        foreign_key="citizens.id"
    )

    citizen: Optional["Citizens"] = Relationship(
        back_populates="issues"
    )


class CreateIssues(SQLModel):
    category: Category
    location: str = Field(max_length=150)
    description: str = Field(max_length=1000)
    citizen_id: int


class ReadIssues(SQLModel):
    id: int
    category: Category
    image_path: Optional[str]
    location: str
    description: str
    status: Status
    created_at: datetime
    citizen_id: int


class UpdateIssueStatus(SQLModel):
    status: Status

class UpdateIssue(SQLModel):
    category: Optional[Category] = None
    location: Optional[str] = Field(default=None, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[Status] = None