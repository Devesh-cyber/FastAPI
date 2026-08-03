from sqlmodel import Session, select, func
from database import get_session
from model import (
    Review, ReviewCreate, ReviewRead, ReviewUpdate
)
from fastapi import APIRouter, Depends, Query, HTTPException

router = APIRouter(prefix='/review', tags=['review'])

@router.post('/', response_model=ReviewRead)
def create_review(review: ReviewCreate, session : Session = Depends(get_session)):
    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get('/', response_model=list[ReviewRead])
def list_reviews(
    play_name: str | None = Query(None, description='Filter by playname'),
    skip: int = Query(0, ge=0, description='Number of reviews to skip'),
    limit: int = Query(10, ge=1, le=50, description='Max reviews to return'),
    session: Session = Depends(get_session)
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)

    query = query.offset(skip).limit(limit)
    reviews = query.exec(query).all()
    return reviews

@router.get('/average/{playname}')
def get_average_rating(play_name: str, session: Session = Depends(get_session)):
    result = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(Review.play_name == play_name)
    ).first()

    avg_rating, total_reviews = result

    if total_reviews == 0:
        raise HTTPException(status_code=404, detail=f'No review found for {play_name}')

    return {
        'play_name' : play_name,
        'average_rating' : round(avg_rating, 2),
        'total_reviews' : total_reviews
    }

@router.get('/{id}')
def get_review_by_id(id: int, session: Session = Depends(get_session)):
    result = session.get(Review, id)
    if not result:
        raise HTTPException(status_code=404, detail='No review')
    return result

@router.patch('/id', response_model=ReviewRead)
def update_review(id:int, update: ReviewUpdate, session : Session = Depends(get_session)):
    review = session.get(Review, id)
    if not review:
        raise HTTPException(status_code=404, detail='No review found')
    
    updated_data  = update.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(review, key, value)

    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.delete('/id')
def delete_review(id:int, session : Session = Depends(get_session)):
    review = session.get(Review, id)
    if not review:
        raise HTTPException(status_code=404, detail='No review found')
    
    session.delete(review)
    session.commit()
    return {'message' : 'Review Deleted'}
