from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

from app.models.analysis_llm import (
    ContractOverview,
    EssentialFields,
    ClauseAnalysis,
    RiskAnalysis
)

from app.prompts.prompt_p1 import (
    CONTRACT_OVERVIEW_PROMPT,
    ESSENTIAL_FIELDS_PROMPT,
    CLAUSE_ANALYSIS_PROMPT,
    RISK_ANALYSIS_PROMPT
)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GOOGLE_API_KEY
)


def create_chain(prompt: str, output_schema):

    prompt_template = ChatPromptTemplate.from_template(prompt)

    structured_llm = llm.with_structured_output(output_schema)

    chain = prompt_template | structured_llm

    return chain


contract_overview_chain = create_chain(
    CONTRACT_OVERVIEW_PROMPT,
    ContractOverview
)


essential_fields_chain = create_chain(
    ESSENTIAL_FIELDS_PROMPT,
    EssentialFields
)

clause_analysis_chain = create_chain(
    CLAUSE_ANALYSIS_PROMPT,
    ClauseAnalysis
)


risk_analysis_chain = create_chain(
    RISK_ANALYSIS_PROMPT,
    RiskAnalysis
)


def analyze_contract(contract_text: str):

    overview = contract_overview_chain.invoke({
        "contract_text": contract_text
    })

    essential_fields = essential_fields_chain.invoke({
        "contract_text": contract_text
    })

    clause_analysis = clause_analysis_chain.invoke({
        "contract_text": contract_text
    })

    risk_analysis = risk_analysis_chain.invoke({
        "contract_text": contract_text
    })

    return {
        "contract_overview": overview,
        "essential_fields": essential_fields,
        "clause_analysis": clause_analysis,
        "risk_analysis": risk_analysis
    }