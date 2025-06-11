from typing import List

from app.db import get_db
from app.schemas import RestaurantCreate, RestaurantRead
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services import RestaurantService

router = APIRouter()


@router.get("/", response_model=List[RestaurantRead])
def list_restaurants(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit
    rows = RestaurantService(db).list_restaurants(offset, limit)

    restaurants = []
    rank = 0
    for r in rows:
        score = 0
        rank += 1
        restaurants.append(
            RestaurantRead(
                id=r.id,
                name=r.name,
                address=r.address,
                cuisine_type=r.cuisine_type,
                sentiment_score=int(score),
                rank=(rank + 1) if rank is not None else None,
            )
        )
    return restaurants

@router.post(
    "/",
    response_model=RestaurantRead,
    status_code=201
)
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):
    return RestaurantService(db).create_restaurant(data)

@router.get(
    "/{restaurant_id}",
    response_model=RestaurantRead,
    status_code=200
)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return RestaurantService(db).get_restaurant_byId(restaurant_id)