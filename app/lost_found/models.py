from sqlalchemy.sql import func
from app.core.db.session import Base
from sqlalchemy import Column, String, Float, Enum, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.lost_found.schema import ItemStatus, ItemType


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(ItemType), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location_lat = Column(String, nullable=False)
    location_lng = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(ItemStatus), default=ItemStatus.open, nullable=False)
    contact_email = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

    matches = relationship("Match", back_populates="item", foreign_keys='Match.item_id')


class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    matched_item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    score = Column(Float, nullable=True)
    matched_on = Column(DateTime(timezone=True), server_default=func.now())
    item = relationship("Item", back_populates="matches", foreign_keys=[item_id])
