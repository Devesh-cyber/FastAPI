from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

from app.service.prompt import (
    CONTRACT_ANALYSIS_PROMPT,
    CLAUSE_EXTRACTION_PROMPT,
    RISK_ASSESSMENT_PROMPT,
    SUMMARY_PROMPT
)

from app.models import (
    ClauseAnalysis,
    RiskFlag,
    AnalysisResult
)

from pydantic import BaseModel
from typing import List


llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    temperature=0
)

class ClauseExtractionResult(BaseModel):
    clauses: List[ClauseAnalysis]


class RiskAssessmentResult(BaseModel):
    risks: List[RiskFlag]


class ContractAnalysisResult(BaseModel):
    summary: str
    contract_type: str
    key_clauses: List[ClauseAnalysis]
    risk_flags: List[RiskFlag]
    overall_risk_level: str
    recommendations: List[str]


# 1. Clause Analysis
contract_prompt = ChatPromptTemplate.from_template(CONTRACT_ANALYSIS_PROMPT)

contract_llm = llm.with_structured_output(ContractAnalysisResult)

contract_analysis_chain = contract_prompt | contract_llm


# 2. Clause Extraction
clause_prompt = ChatPromptTemplate.from_template(
    CLAUSE_EXTRACTION_PROMPT
)

clause_llm = llm.with_structured_output(ClauseExtractionResult)

clause_extraction_chain = (
    clause_prompt
    | clause_llm
)

# 3. Risk Assesment Chain

risk_prompt = ChatPromptTemplate.from_template(
    RISK_ASSESSMENT_PROMPT
)

risk_llm = llm.with_structured_output(
    RiskAssessmentResult
)

risk_assesment_chain = risk_prompt | risk_llm


# 4. Sumary Chain

summary_prompt = ChatPromptTemplate.from_template(
    SUMMARY_PROMPT
)

summary_chain = summary_prompt | llm
