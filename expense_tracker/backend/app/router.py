from fastapi import APIRouter, Depends
from app.database import get_session
from sqlmodel import Session
from app.models import ExpenseTracker, ExpenseTrackerCreate, ExpenseTrackerRead

router = APIRouter(
    prefix='/expense',
    tags=['Expense']
)


@router.post('/', response_model=ExpenseTrackerRead)
def create_tracker(expense: ExpenseTrackerCreate, session: Session = Depends(get_session)):
    expense_data = ExpenseTracker(**expense.model_dump())
    session.add(expense_data)
    session.commit()
    session.refresh(expense_data)
    return expense_data