from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Analysis(SQLModel, table=True):
    """
    Analysis Model
    """

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    contract_id: int = Field(
        foreign_key="contract.id",
        unique=True,
        index=True
    )

    result: str

    model_name: str

    prompt_version: str

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now
    )


class AnalysisRead(SQLModel):
    """
    Read Analysis Model
    """

    id: int
    contract_id: int
    result: str
    model_name: str
    prompt_version: str
    created_at: datetime
    updated_at: datetime