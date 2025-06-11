from typing import Optional

from pydantic import BaseModel, Field

# RESTAURANT ------------------------------------------------------------------

class RestaurantRead(BaseModel):
    id: int
    name: str
    address: Optional[str]
    cuisine_type: Optional[str]
    extra_data: Optional[dict] = Field(None, description="Extra JSON data")
    sentiment_score: int = 0   # default 0 on creation
    rank: Optional[int] = None


class RestaurantCreate(BaseModel):
    name: str
    address: Optional[str]
    cuisine_type: Optional[str]
    extra_data: Optional[dict]


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    cuisine_type: Optional[str] = None
    metadata: Optional[dict] = None



# REVIEWS ------------------------------------------------------------------

class ReviewRead(BaseModel):
    id: int
    restaurant_id: int
    text: str
    rating: int
    sentiment: str
    sentiment_score: float | None

class ReviewCreate(BaseModel):
    text: str
    rating: int
