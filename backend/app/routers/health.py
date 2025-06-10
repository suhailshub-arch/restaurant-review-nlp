from app.db import engine
from fastapi import APIRouter
from sqlalchemy import text

router = APIRouter()


@router.get("/healthz", status_code=200)
def health_check():
    with engine.connect() as con:
        con.execute(text("SELECT 1;"))

    return {"status": "ok", "db": "reachable"}
