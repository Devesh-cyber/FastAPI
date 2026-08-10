from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form, File
from database import get_session
from sqlmodel import Session, select
from models.issues import (
    Issues,
    CreateIssues,
    ReadIssues,
    UpdateIssueStatus,
    UpdateIssue,
    Category
    )
from models.citizen import (
    ReadCitizens, 
    Citizens
)
from auth import verify_api_key
from image_processing import upload_image
from typing import Optional

router = APIRouter(
    prefix='/Issues',
    tags=['Issues']
)

@router.post('/', response_model=ReadIssues)
async def create_issues(
    category: Category = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    citizen_id: int = Form(...),
    image: UploadFile = File(...),
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    citizen = session.get(Citizens, citizen_id)
    
    if not citizen:
        raise HTTPException(
                status_code=404,
                detail="Citizen not found"
            )
    
    image_path = await upload_image(image)

    issues = Issues(
        category=category,
        location=location,
        description=description,
        citizen_id=citizen_id,
        image_path=image_path
    )

    session.add(issues)
    session.commit()
    session.refresh(issues)
    return issues


@router.get('/{id}',response_model=ReadIssues)
def read_issue_by_id(
    id: int,
    session: Session = Depends(get_session)
):    
    issue = session.get(Issues, id)
    if not issue:
        raise HTTPException(status_code=404, detail='Issue Not Found')
    return issue


@router.patch('/{id}', response_model=ReadIssues)
def update_issue(
    id: int,
    updated_data: UpdateIssue,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    issue = session.get(Issues, id)
    if not issue:
        raise HTTPException(status_code=404, detail='Issue Not Found')
    
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(issue, key, value)

    session.add(issue)
    session.commit()
    session.refresh(issue)
    return issue


@router.delete('/{id}')
def delete_issue(
    id: int,
    session: Session = Depends(get_session)
):
    issue = session.get(Issues, id)
    if not issue:
        raise HTTPException(status_code=404, detail='Issue Not Found')
    
    session.delete(issue)
    session.commit()
    return {'message': 'Issue Deleted Successfully'}


@router.get('/', response_model=list[ReadIssues])
def read_issues(
    filter_category: Optional[Category] = None,
    filter_status: Optional[str] = None,
    filter_location: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Issues)
    if filter_category:
        query = query.where(Issues.category == filter_category)
    if filter_status:
        query = query.where(Issues.status == filter_status)
    if filter_location:
        query = query.where(Issues.location == filter_location)
    
    issues = session.exec(query).all()
    if not issues:
        raise HTTPException(status_code=404, detail='No Issues Found')
    return issues