from fastapi import APIRouter, Depends, HTTPException, Query
from auth import verify_api_key
from database import get_session
from sqlmodel import Session, select
from models.books import Books, BooksCreate, BooksRead, BookUpdate
from typing import Optional

router = APIRouter(
    prefix='/books',
    tags=['Books']
)

@router.get('/', response_model=list[BooksRead])
def list_books(
    title: Optional[str] = Query(default=None),
    author: Optional[str] = Query(None),
    session: Session = Depends(get_session)
    ):

    query = select(Books).where(
        Books.is_sold == False
    )

    if title:
        query = query.where(Books.title.contains(title))

    if author:
        query = query.where(Books.author.contains(author))

    books = session.exec(query).all()
    return books


@router.post('/', response_model=BooksRead)
def create_book(
    book_data: BooksCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):

    book = Books.model_validate(book_data)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.patch('/{book_id}', response_model=BooksRead)
def update_book(
    book_id: int,
    updates: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):

    book = session.get(Books, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='Book Not found')

    book_data = updates.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.patch('/{book_id}/sold', response_model=BooksRead)
def mark_book_sold(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):

    book = session.get(Books, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='Book Not Found')

    book.is_sold = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book