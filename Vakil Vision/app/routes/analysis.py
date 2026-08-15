from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session

from app.models.contract import Contract, ContractStatus
from app.models.analysis import Analysis, AnalysisRead

from app.service.gemini_analyze import run_contract_analysis
import traceback

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.post(
    "/{contract_id}",
    response_model=AnalysisRead
)
def create_analysis(
    contract_id: int,
    session: Session = Depends(get_session)
):

    # -------------------------
    # Get contract
    # -------------------------

    contract = session.get(Contract, contract_id)

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )


    # -------------------------
    # Check extracted text
    # -------------------------

    if not contract.raw_text:

        raise HTTPException(
            status_code=400,
            detail="Contract has no extracted text"
        )


    # -------------------------
    # Check existing analysis
    # -------------------------

    existing_analysis = session.query(Analysis).filter(
        Analysis.contract_id == contract_id
    ).first()

    if existing_analysis:

        raise HTTPException(
            status_code=409,
            detail="Contract has already been analyzed"
        )


    # -------------------------
    # Processing
    # -------------------------

    contract.status = ContractStatus.processing

    session.add(contract)
    session.commit()
    session.refresh(contract)


    try:

        # -------------------------
        # Run AI analysis
        # -------------------------

        final_report = run_contract_analysis(
            contract.raw_text
        )


        # -------------------------
        # Save analysis
        # -------------------------

        analysis = Analysis(
            contract_id=contract.id,
            result=final_report.model_dump_json(),
            model_name="gemini-2.5-flash",
            prompt_version="v1"
        )

        session.add(analysis)


        # -------------------------
        # Update contract
        # -------------------------

        contract.status = ContractStatus.analyzed

        session.add(contract)

        session.commit()
        session.refresh(analysis)

        return analysis


    except Exception as e:
    

        traceback.print_exc()

        contract.status = ContractStatus.failed
        session.add(contract)
        session.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Contract analysis failed: {str(e)}"
        )