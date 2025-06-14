from typing import List

from redis import Redis

from app.db import get_db
from app.schemas import RestaurantCreate, RestaurantRead, RestaurantUpdate
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services.restaurant_service import RestaurantService
from app.redis import get_redis

router = APIRouter()


@router.get("/", response_model=List[RestaurantRead])
def list_restaurants(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
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
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    created =  RestaurantService(db).create_restaurant(data)

    redis.zadd("restaurant_leaderboard", {str(created.id): 0})
    return created

@router.get(
    "/{restaurant_id}",
    response_model=RestaurantRead,
    status_code=200
)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return RestaurantService(db).get_restaurant_byId(restaurant_id)

@router.patch(
    "/{restaurant_id}",
    status_code=204
)
def update_restaurant(restaurant_id: int, data: RestaurantUpdate, db: Session = Depends(get_db)):
    RestaurantService(db).update_restaurant(restaurant_id, data)
    return 

@router.delete(
    "/{restaurant_id}",
    status_code=200,
    response_model=dict
)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    RestaurantService(db).delete_restaurant(restaurant_id)
    return {"message" : f"Restaurant {restaurant_id} deleted successfully"}