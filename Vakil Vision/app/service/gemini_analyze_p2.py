from app.prompts.prompt_p2 import FINAL_REPORT_PROMPT

from app.models.analysis_llm import FinalReport

from app.service.gemini_analyze_p1 import create_chain


final_report_chain = create_chain(
    FINAL_REPORT_PROMPT,
    FinalReport
)


def generate_final_report(analyses):

    final_report = final_report_chain.invoke({
        "contract_overview": analyses["contract_overview"].model_dump_json(),
        "essential_fields": analyses["essential_fields"].model_dump_json(),
        "clause_analysis": analyses["clause_analysis"].model_dump_json(),
        "risk_analysis": analyses["risk_analysis"].model_dump_json()
    })

    return final_report