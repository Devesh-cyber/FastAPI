from fastapi import APIRouter, FastAPI, Depends
from sqlmodel import SQLModel, Session, select
from app.database import get_session
from app.models import ExpenseTrackerAnalysis, ExpenseTracker

router = APIRouter(prefix='/analysis', tags=['Analysis'])

@router.get('/', response_model=ExpenseTrackerAnalysis)
def analye_expense(session: Session = Depends(get_session)):
    analysis = session.exec(select(ExpenseTracker)).all()
    total_transactions = len(analysis)
    total_expense = sum(e.amount for e in analysis)
    average_expense = total_expense / total_transactions
    highest_expense = max(e.amount for e in analysis)
    return ExpenseTrackerAnalysis(
        total_transactions=total_transactions,
        total_expense=total_expense,
        average_expense=average_expense,
        highest_expense=highest_expense
    )

    