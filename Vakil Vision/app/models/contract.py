from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ContractStatus(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    analyzed = "analyzed"
    failed = "failed"


class Contract(SQLModel, table=True):
    """
    Contract Model
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="user.id",
        index=True
    )

    title: str = Field(min_length=1)

    filename: str
    filetype: str

    raw_text: Optional[str] = None

    status: ContractStatus = Field(
        default=ContractStatus.uploaded
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )


class ContractRead(SQLModel):
    """
    Read Contract Model
    """

    id: int
    user_id: int
    title: str
    filename: str
    filetype: str
    status: ContractStatus
    created_at: datetime
    