from typing import List, Optional
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class ItemType(str, Enum):
    lost = "lost"
    found = "found"

class ItemStatus(str, Enum):
    open = "open"
    resolved = "resolved"


class ItemBase(BaseModel):
    type: ItemType
    title: str
    description: str
    location_lat: str
    location_lng: str
    contact_email: str
    contact_name: str
    image_url: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemOut(ItemBase):
    id: UUID
    timestamp: datetime
    status: ItemStatus

    class Config:
        from_attributes = True


class MatchOut(BaseModel):
    id: UUID
    item_id: UUID
    matched_item_id: UUID
    score: Optional[float] = None
    matched_on: datetime

    class Config:
        from_attributes = True

class ItemListResponse(BaseModel):
    count: int
    items: List[ItemOut]
