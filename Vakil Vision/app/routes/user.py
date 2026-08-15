from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from sqlmodel import Session, select
from app.models.user import UserRead, User, UserCreate


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/', response_model=UserRead)
def create_user(userData: UserCreate, session: Session = Depends(get_session)):
    '''
    Create User
    '''
    user = User(**userData.model_dump())

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get('/', response_model=list[UserRead])
def read_user(session: Session = Depends(get_session)):
    '''
    Read User
    '''
    user = session.exec(select(User)).all()
    return user


@router.get('/{id}', response_model=UserRead)
def read_user_by_id(id: int, session: Session = Depends(get_session)):
    '''
    Read User by Id
    '''
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail=f'No record with id {id} found')
    return user
