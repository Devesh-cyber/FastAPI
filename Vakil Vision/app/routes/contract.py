from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.database import get_session
from sqlmodel import Session, select
from app.models.contract import Contract, ContractRead, ContractStatus
from app.models.user import User
from app.service.contract_upload import upload_file

router = APIRouter(
    prefix='/contract',
    tags=['Contract']
)


@router.post('/', response_model=ContractRead)
async def upload_contract_file(user_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    '''
    Upload the file contract
    '''

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with id {user_id} not found'
        )

    data = await upload_file(file)

    contract = Contract(
        user_id=user_id,
        title=file.filename,
        filename=data['filename'],
        filetype=data['filetype'],
        raw_text=data['raw_text'],
        status=ContractStatus.uploaded
    )

    session.add(contract)
    session.commit()
    session.refresh(contract)
    return contract


@router.get('/', response_model=list[ContractRead])
def list_all_contracts(session: Session = Depends(get_session)):
    '''
    List all the contracts
    '''

    contract = session.exec(select(Contract)).all()
    return contract


@router.get('/{id}', response_model=ContractRead)
def contract_by_id(id: int, session: Session = Depends(get_session)):
    '''
    Get contract by id
    '''

    contract = session.get(Contract, id)

    if not contract:
        raise HTTPException(status_code=404, detail=f'The given contract id {id} not has any contract')
    return contract


@router.get('/{user_id}/contracts', response_model=list[ContractRead])
def contract_by_user_id(user_id: int, session: Session = Depends(get_session)):
    '''
    Get contract from user_id
    '''

    contract = session.exec(
        select(Contract).where(Contract.user_id == user_id)
        ).all()

    if not contract:
            raise HTTPException(status_code=404, detail=f'The given contract id {id} not has any contract')
    return contract
