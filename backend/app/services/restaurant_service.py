from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from ..models import Restaurant
from ..schemas import RestaurantCreate, RestaurantRead, RestaurantUpdate

class RestaurantService:
    def __init__(self, db: Session):
        self.db = db

    def create_restaurant(self, data: RestaurantCreate) -> Restaurant:
        new_rest = Restaurant(
            name=data.name,
            address=data.address,
            cuisine_type=data.cuisine_type,
            extra_data=data.extra_data
        )
        self.db.add(new_rest)
        try:
            self.db.commit()
            self.db.refresh(new_rest)
        except IntegrityError as e:
            self.db.rollback()
            # handle unique constraint on `name`
            if "unique constraint" in str(e.orig).lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Restaurant with name '{data.name}' already exists."
                )
            raise
        return new_rest

    def list_restaurants(self, offset: int, limit: int) -> List[RestaurantRead]:
        return self.db.query(Restaurant).offset(offset).limit(limit).all()

    def get_restaurant_byId(self, restaurant_id: int) -> RestaurantRead:
        rest = self.db.query(Restaurant).where(Restaurant.id==restaurant_id).first()
        if rest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant Not Found"
            )
        return rest
    
    def update_restaurant(self, restaurant_id: int, data: RestaurantUpdate) -> Restaurant:
        rest = self.get_restaurant_byId(restaurant_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rest, field, value)
        self.db.commit()
        self.db.refresh(rest)
        return rest
    
    def delete_restaurant(self, restaurant_id: int) -> None:
        rest = self.get_restaurant_byId(restaurant_id)
        self.db.delete(rest)
        self.db.commit()