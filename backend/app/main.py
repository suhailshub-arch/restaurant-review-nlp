from fastapi import FastAPI

from app.routers import health
from .db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Restaurant Review API")

app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}