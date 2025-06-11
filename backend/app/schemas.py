from typing import Optional

from pydantic import BaseModel, Field


class RestaurantRead(BaseModel):
    id: int
    name: str
    address: Optional[str]
    cuisine_type: Optional[str]
    extra_data: Optional[dict] = Field(None, description="Extra JSON data")
    sentiment_score: int = 0   # default 0 on creation
    rank: Optional[int] = None

    class Config:
        orm_mode = True

class RestaurantCreate(BaseModel):
    name: str
    address: Optional[str]
    cuisine_type: Optional[str]
    extra_data: Optional[dict]

    class Config:
        orm_mode = True