FINAL_REPORT_PROMPT = """
You are analyzing a legal contract based on the structured analysis
already performed on the contract.

Using the four analysis results below, produce the final detailed report.

Your report must contain:

1. Key Findings
   - Identify the most important findings from the analysis.
   - Explain why each finding matters.
   - Reference the relevant clause where applicable.

2. Recommendations
   - Provide practical recommendations based on the identified risks
     and important contractual terms.
   - Prioritize recommendations according to their importance.

3. Summary
   - Provide a concise overall summary of the contract.
   - Mention the most significant obligations, risks, and considerations.

Do not invent information.
Do not introduce facts that are not present in the provided analyses.
Base the final report only on the provided analysis results.

Contract Overview:
{contract_overview}

Essential Fields:
{essential_fields}

Clause Analysis:
{clause_analysis}

Risk Analysis:
{risk_analysis}
"""