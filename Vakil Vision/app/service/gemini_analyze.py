from app.service.gemini_analyze_p1 import analyze_contract
from app.service.gemini_analyze_p2 import generate_final_report


def run_contract_analysis(contract_text: str):

    analyses = analyze_contract(contract_text)

    final_report = generate_final_report(analyses)

    return final_report