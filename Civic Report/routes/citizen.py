from fastapi import APIRouter, HTTPException, Depends
from database import get_session
from sqlmodel import Session, select
from models.citizen import (
    Citizens, 
    CreateCitizens, 
    ReadCitizens, 
    UpdateCitizens)
from models.issues import ReadIssues
from auth import verify_api_key

router = APIRouter(
    prefix='/Citizens',
    tags=['Citizens']
)

@router.post('/', response_model=ReadCitizens)
def create_citizens(
    citizen_data: CreateCitizens,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):

    citizen = Citizens(**citizen_data.model_dump())

    session.add(citizen)
    session.commit()
    session.refresh(citizen)
    return citizen


@router.get('/', response_model=list[ReadCitizens])
def read_citizens(
    session: Session = Depends(get_session)
):
    citizen = session.exec(select(Citizens)).all()

    if not citizen:
        raise HTTPException(status_code=404, detail='Citizen Not Found')
    return citizen


@router.get('/{id}', response_model=ReadCitizens)
def read_citizen_by_id(
    id: int,
    session: Session = Depends(get_session)
):
    citizen = session.get(Citizens, id)
    if not citizen:
        raise HTTPException(status_code=404, detail='Citizen Not Found')
    return citizen


@router.get('/{id}/issues', response_model=list[ReadIssues])
def read_citizen_issues(
    id: int,
    session: Session = Depends(get_session)
):
    citizen = session.get(Citizens, id)
    if not citizen:
        raise HTTPException(status_code=404, detail='Citizen Not Found')
    return citizen.issues