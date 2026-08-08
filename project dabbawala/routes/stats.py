from datetime import date, datetime
from fastapi import APIRouter, Depends, Query
from model import OrderStatus, StatusLog, Order
from sqlmodel import Session, func, select
from database import get_session


router = APIRouter(prefix='/stats', tags=['Stats'])

@router.get('/daily_orders')
def daily_summary(
    summary_date: date | None = Query(None, description='Date for summary (YYYY_MM-DD)'),
    session: Session = Depends(get_session)
):
    if summary_date is None:
        summary_date = date.today()

    start = datetime.combine(summary_date, datetime.min.time())
    end = datetime.combine(summary_date, datetime.max.time())

    summary = {}
    total = 0

    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id).where(Order.created_at >= start, Order.created_at <= end, Order.status == status))
        ).one()

        summary[status.value] = count
        total += count

    return {
        'date' : summary_date.isoformat(),
        'total_orders' : total,
        'by_status' : summary
    }