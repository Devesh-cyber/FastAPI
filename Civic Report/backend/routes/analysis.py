from fastapi import APIRouter, HTTPException, Depends
from database import get_session
from sqlmodel import Session, select, func

from models.issues import ReadIssues, Issues, Category, UpdateIssueStatus, UpdateIssue
from models.citizen import Citizens


router = APIRouter(
    prefix='/Analysis',
    tags=['Analysis']
)


@router.get('/stats')
def get_statistics(
    session: Session = Depends(get_session)
):
    total_citizens = len(session.exec(select(Citizens)).all())
    total_issues = len(session.exec(select(Issues)).all())

    issues_by_category = session.exec(
        select(Issues.category, func.count(Issues.id))
        .group_by(Issues.category)
    ).all()

    issues_by_status = session.exec(
        select(Issues.status, func.count(Issues.id))
        .group_by(Issues.status)
    ).all()

    return {
        "total_citizens": total_citizens,
        "total_issues": total_issues,
        "issues_by_category": dict(issues_by_category),
        "issues_by_status": dict(issues_by_status)
    }