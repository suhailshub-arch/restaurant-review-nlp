from app.db import engine
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from redis import Redis

from app.redis import get_redis

router = APIRouter(tags=["healthz"])


@router.get("/", status_code=200)
def health_check():
    with engine.connect() as con:
        con.execute(text("SELECT 1;"))

    return {"status": "ok", "db": "reachable"}

@router.get("/redis-test")
def redis_test(redis: Redis = Depends(get_redis)):
    try:
        redis.set("healthcheck", "ok", ex=5)
        val = redis.get("healthcheck")
        if val != "ok":
            raise RuntimeError("Unexpected value")
        return {"redis": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis error: {e}")