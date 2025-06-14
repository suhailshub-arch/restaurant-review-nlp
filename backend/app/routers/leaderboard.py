from typing import List
from fastapi import APIRouter, Depends, Query
from redis import Redis
from sqlalchemy.orm import Session
from app.redis import get_redis
from app.schemas import LeaderboardEntry
from app.db import get_db
from app.models import Restaurant


router = APIRouter()

@router.post("/init/{restaurant_id}", status_code=204)
def init_score(
    restaurant_id: int,
    redis: Redis = Depends(get_redis)
):
    redis.zadd("restaurant_leaderboard", {str(restaurant_id): 0})
    return

@router.get("/", response_model=List[LeaderboardEntry])
def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    redis: Redis = Depends(get_redis),
    db: Session = Depends(get_db)
):
    raw = redis.zrevrange("restaurant_leaderboard", 0, limit-1, withscores=True)
    if not raw:
        return []
    
    entries = []
    for rank, (member, score) in enumerate(raw, start=1):
        rest = db.query(Restaurant).get(int(member))
        if not rest:
            redis.zrem("restaurant_leaderboard", member)
            continue
        entries.append(
            LeaderboardEntry(
                restaurant_id=int(member),
                name=rest.name,
                sentiment_score=int(score),
                rank=rank
            )
        )

    return entries