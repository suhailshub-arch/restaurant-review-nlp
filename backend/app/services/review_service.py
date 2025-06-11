from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas import ReviewCreate, ReviewRead, ReviewUpdate
from app.models import Review

class ReivewService:
    def __init__(self, db: Session):
        self.db = db

    def list_reviews(self, restaurant_id: int, offset: int, limit: int) -> List[ReviewRead]:
        reviews = self.db.query(Review).where(Review.restaurant_id == restaurant_id).offset(offset).limit(limit).all()
        if reviews == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Reviews For This Restaurant"
            )
        return reviews
    
    def create_review(self, data: ReviewCreate, restaurant_id: int) -> Review:
        new_review = Review(
            restaurant_id = restaurant_id,
            text = data.text,
            rating = data.rating
        )
        self.db.add(new_review)
        try:
            self.db.commit()
            self.db.refresh(new_review)
        except:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inserting review"
            )
        return new_review
    

    def list_review_byId(self, review_id: int) -> ReviewRead:
        review = self.db.query(Review).where(Review.id==review_id).first()
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Review Not Found"
            )
        return review
    

    def update_review(self, review_id: int, data: ReviewUpdate) -> Review:
        review = self.list_review_byId(review_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(review, field, value)

        self.db.commit()
        self.db.refresh(review)
        return