CONTRACT_OVERVIEW_PROMPT = """
Analyze the following legal contract and provide a clear overview.

Identify:
- Type of contract
- Purpose of the contract
- All parties involved
- Effective date
- Expiry date
- Governing law

Only use information explicitly present in the contract.
If a field is not available, return null.

Contract:
{contract_text}
"""

ESSENTIAL_FIELDS_PROMPT = """
Analyze the following legal contract and extract its essential terms.

Identify:
- Payment terms
- Contract duration
- Renewal terms
- Termination terms
- Notice period
- Penalties
- Important dates

Only use information explicitly present in the contract.
Do not invent or assume missing information.

Contract:
{contract_text}
"""

CLAUSE_ANALYSIS_PROMPT = """
Analyze the following legal contract clause by clause.

For each important clause:
- Identify the clause title
- Extract the relevant clause text
- Explain what the clause means
- Explain its purpose
- Explain why the clause is important

Focus on clauses that materially affect the rights, obligations,
financial exposure, termination, liability, confidentiality,
intellectual property, dispute resolution, or other significant
contractual obligations of the parties.

Only use information explicitly present in the contract.

Contract:
{contract_text}
"""

RISK_ANALYSIS_PROMPT = """
Analyze the following legal contract for potential risks.

For every significant risk:
- Give the risk a title
- Assign a severity
- Explain the risk
- Identify the affected party
- Identify the clause causing the risk
- Provide a practical recommendation

Also provide an overall assessment of the contract's risk level.

Do not invent risks that are not supported by the contract.
Base every identified risk on specific contractual language.

Contract:
{contract_text}
"""

