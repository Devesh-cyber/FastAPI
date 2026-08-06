from fastapi import APIRouter, Depends, Query, HTTPException
from app.database import get_session
from app.models import ExpenseTrackerList, ExpenseTracker
from app.enum import ExpenseCategory, PaymentMethod
from typing import Optional, Literal
from datetime import date
from sqlmodel import select, Session
from sqlalchemy import or_

router = APIRouter(
    prefix='/expenses/operations',
    tags=['Opeartions']
)


@router.get('/filter',response_model=ExpenseTrackerList)
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


@router.get('/search', response_model=ExpenseTrackerList)
def search_transactions(search: str = Query(None, description='Enter the value which u have to search over transactions'), session: Session = Depends(get_session)):
    query = select(ExpenseTracker).where(
         or_(
              ExpenseTracker.title.ilike(f"%{search}%"),
              ExpenseTracker.description.ilike(f"%{search}%")
         )
    )

    expense = session.exec(query).all()

    if len(expense) == 0:
         raise HTTPException(status_code=404, detail=f'No such transactions found with {search} keyword')
    return ExpenseTrackerList(
         count = len(expense),
         transactions=expense
    )


@router.get('/sorting', response_model=ExpenseTrackerList)
def sort_transactions(sort_by: Literal['amount','created_at'] = Query(..., description='The field to sort transactiions on'), 
                      order: Literal['asc', 'desc'] = Query('asc', description='The order in which u wish to see the result'),
                      session: Session = Depends(get_session)):
    fields = {
        "amount": ExpenseTracker.amount,
        "expense_date": ExpenseTracker.expense_date,
    }

    statement = select(ExpenseTracker)

    sort_field = fields.get(sort_by)

    if sort_field:
        if order == "asc":
            statement = statement.order_by(sort_field.asc())
        else:
            statement = statement.order_by(sort_field.desc())

    expenses = session.exec(statement).all()

    return ExpenseTrackerList(
        count=len(expenses),
        transactions=expenses,
    )