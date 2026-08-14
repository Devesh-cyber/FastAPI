from pydantic import BaseModel, Field
from typing import Optional, List
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

   
class ClauseAnalysis(BaseModel):
    clause_title: str
    clause_text: str
    explanation: str
    is_standard: bool


class RiskFlag(BaseModel):
    risk_title: str
    description: str
    risk_level: str
    recommendation: str
    clause_reference: str


class AnalysisResult(BaseModel):
    contract_id: str = ""
    summary: str
    contract_type: str
    key_clauses: List[ClauseAnalysis]
    risk_flags: List[RiskFlag]
    overall_risk_level: str
    recommendations: List[str]