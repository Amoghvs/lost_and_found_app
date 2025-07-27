from typing import List
from pydantic import BaseModel

from app.lost_found.schema import ItemOut


class MatchedItem(BaseModel):
    match_score: float
    item: ItemOut  # Reuse your existing ItemOut model

    class Config:
        from_attributes = True


class MatchedLostItem(BaseModel):
    match_score: float
    lost_item: ItemOut  # already has orm_mode

    class Config:
        from_attributes = True  # Ensure it can read from attributes

class MatchListResponse(BaseModel):
    count: int
    items: List[MatchedLostItem]
