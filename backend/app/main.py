from app.routers import admin, health, leaderboard, restaurants, reviews
from fastapi import FastAPI


app = FastAPI(title="Restaurant Review API")

app.include_router(health.router, prefix="/healthz")
app.include_router(restaurants.router, prefix="/api/v1/restaurants")
app.include_router(reviews.router)
app.include_router(leaderboard.router, prefix="/api/v1/leaderboard")
app.include_router(admin.router, prefix="/api/v1/admin")


@app.get("/")
async def root():
    return {"message": "Restaurant Review API"}
