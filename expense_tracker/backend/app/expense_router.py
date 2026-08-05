from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from sqlmodel import Session, select, func
from app.models import ExpenseTracker, ExpenseTrackerCreate, ExpenseTrackerRead, ExpenseTrackerList, ExpenseTrackerUpdate
from typing import Optional
from app.enum import ExpenseCategory, PaymentMethod
from datetime import date

router = APIRouter(
    prefix='/expenses',
    tags=['Expense']
)


@router.post('/create', response_model=ExpenseTrackerRead)
def create_tracker(expense: ExpenseTrackerCreate, session: Session = Depends(get_session)):
    expense_data = ExpenseTracker(**expense.model_dump())
    session.add(expense_data)
    session.commit()
    session.refresh(expense_data)
    return expense_data


@router.get('/view/{id}', response_model=ExpenseTrackerRead)
def read_tracker(id: int, session: Session = Depends(get_session)):
    res = session.exec(select(ExpenseTracker).where(ExpenseTracker.id == id)).first()
    if not res:
        raise HTTPException(status_code=404, detail=f'Id {id} not found in the db')
    return res

@router.get('/view', response_model=ExpenseTrackerList)
def read_all_tracker(session: Session = Depends(get_session)):
    expenses = session.exec(select(ExpenseTracker)).all()
    if not expenses:
        raise HTTPException(status_code=404, detail=f'No Expenses Transactions retrieved')
    return ExpenseTrackerList(
        count=len(expenses),
        transactions=expenses
    )

@router.delete('/remove/{id}')
def remove_expense(id: int, session: Session = Depends(get_session)):
    expense = session.get(ExpenseTracker, id)
    if not expense:
            raise HTTPException(status_code=404, detail='No transaction found')
    session.delete(expense)
    session.commit()
    return {'Message': 'The field got deleted'}


@router.patch('/update/{id}', response_model=ExpenseTrackerRead)
def update_expense(id: int, updated_exp: ExpenseTrackerUpdate, session: Session = Depends(get_session)):
    expense = session.get(ExpenseTracker, id)
    if not expense:
        raise HTTPException(status_code=404, detail=f'No transaction with {id} found')
    updated_exp = updated_exp.model_dump(exclude_unset=True)

    for key, value in updated_exp.items():
         setattr(expense, key, value)

    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


@router.get('/operations',response_model=ExpenseTrackerList)
def get_expenses(
     category: Optional[ExpenseCategory] = None,
     payment_method: Optional[PaymentMethod] = None,
     min_amount: Optional[float] = None,
     max_amount: Optional[float] = None,
     expense_date: Optional[date] = None,
     session: Session = Depends(get_session)
):
    query = select(ExpenseTracker)

    if category:
          query = query.where(ExpenseTracker.category == category)

    if payment_method:
         query = query.where(ExpenseTracker.payment_method == payment_method)

    if min_amount is not None:
         query = query.where(ExpenseTracker.amount >= min_amount)

    if max_amount is not None:
         query = query.where(ExpenseTracker.amount <= max_amount) 

    if expense_date:
         query = query.where(ExpenseTracker.expense_date == expense_date)

    expenses = session.exec(query).all()

    return ExpenseTrackerList(
    count=len(expenses),
    transactions=expenses
)