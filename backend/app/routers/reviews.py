from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas import ReviewCreate, ReviewRead, ReviewUpdate
from app.db import get_db
from app.services.review_service import ReivewService

router = APIRouter()

@router.get(
    "/api/v1/restaurants/{restaurant_id}/reviews", 
    response_model=List[ReviewRead]
)
def get_reviews(
    restaurant_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    rows = ReivewService(db).list_reviews(restaurant_id, offset, limit)

    reviews = []
    for r in rows:
        reviews.append(
            ReviewRead(
                id=r.id,
                restaurant_id= r.restaurant_id,
                text= r.text,
                rating= r.rating,
                sentiment= r.sentiment,
                sentiment_score= r.sentiment_score,
            )
        )

    return reviews

@router.post(
    "/api/v1/restaurants/{restaurant_id}/reviews", 
    response_model=ReviewRead,
    status_code=201
)
def create_review(data: ReviewCreate, restaurant_id: int, db: Session = Depends(get_db)):
    return ReivewService(db).create_review(data, restaurant_id)

@router.get(
    "/api/v1/reviews/{review_id}",
    status_code=200,
    response_model=ReviewRead
)
def get_review_byId(review_id: int, db: Session = Depends(get_db)):
    return ReivewService(db).list_review_byId(review_id)

@router.patch(
    "/api/v1/reviews/{review_id}",
    status_code=204
)
def update_review(review_id: int, data: ReviewUpdate, db: Session = Depends(get_db)):
    ReivewService(db).update_review(review_id, data)

@router.delete(
    "/api/v1/reviews/{review_id}",
    response_model=dict,
    status_code=200
)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    ReivewService(db).delete_review(review_id)
    return {"message": f"Review {review_id} deleted successfully"}