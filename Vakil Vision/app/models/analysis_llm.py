from pydantic import BaseModel, Field
from typing import Optional


# -------------------------
# Contract Overview
# -------------------------

class ContractOverview(BaseModel):
    contract_type: str
    purpose: str
    parties: list[str]
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None
    governing_law: Optional[str] = None


# -------------------------
# Essential Fields
# -------------------------

class EssentialFields(BaseModel):
    payment_terms: Optional[str] = None
    contract_duration: Optional[str] = None
    renewal_terms: Optional[str] = None
    termination_terms: Optional[str] = None
    notice_period: Optional[str] = None
    penalties: Optional[str] = None
    important_dates: list[str] = Field(default_factory=list)


# -------------------------
# Key Data
# -------------------------

class KeyDataItem(BaseModel):
    key: str
    value: str
    importance: str


class KeyData(BaseModel):
    items: list[KeyDataItem]


# -------------------------
# Clause Analysis
# -------------------------

class ClauseAnalysisItem(BaseModel):
    clause_title: str
    clause_text: str
    explanation: str
    purpose: str
    importance: str


class ClauseAnalysis(BaseModel):
    clauses: list[ClauseAnalysisItem]


# -------------------------
# Risk Analysis
# -------------------------

class RiskItem(BaseModel):
    title: str
    severity: str
    explanation: str
    affected_party: str
    source_clause: str
    recommendation: str


class RiskAnalysis(BaseModel):
    overall_risk: str
    risks: list[RiskItem]


# -------------------------
# Key Findings
# -------------------------

class FindingItem(BaseModel):
    title: str
    description: str
    importance: str
    source_clause: str


class KeyFindings(BaseModel):
    findings: list[FindingItem]


# -------------------------
# Recommendations
# -------------------------

class RecommendationItem(BaseModel):
    title: str
    recommendation: str
    reason: str
    priority: str


class Recommendations(BaseModel):
    recommendations: list[RecommendationItem]


# -------------------------
# Complete LLM Output
# -------------------------

class AnalysisOutput(BaseModel):
    contract_overview: ContractOverview
    essential_fields: EssentialFields
    key_data: KeyData
    clause_analysis: ClauseAnalysis
    risk_analysis: RiskAnalysis
    key_findings: KeyFindings
    recommendations: Recommendations
    summary: str


class FinalReport(BaseModel):
    key_findings: KeyFindings
    recommendations: Recommendations
    summary: str