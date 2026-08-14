from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Contract(BaseModel):

    id: Optional[str] = None
    filename: str
    original_name: str
    upload_date: datetime = Field(default_factory=datetime.now)
    text_content: str  = ''
    page_count: int = 0
    word_count: int = 0
    status: str = 'uploaded'

   