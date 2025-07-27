from uuid import UUID
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.match.schema import MatchedLostItem, MatchListResponse
from app.core.db.session import get_db
from app.lost_found import models
from app.lost_found.schema import ItemOut
from fastapi import APIRouter, Depends, HTTPException


match_router = APIRouter(prefix="/matches", tags=["matches"])

# @match_router.get("/{item_id}", response_model=List[ItemOut])
# def match_item(item_id: UUID, db: Session = Depends(get_db)):
#     new_item = db.query(models.Item).filter(models.Item.id == item_id).first()
#     if not new_item:
#         raise HTTPException(status_code=404, detail="Item not found")

#     opposite_type = models.ItemType.found if new_item.type == models.ItemType.lost else models.ItemType.lost
#     candidates = db.query(models.Item).filter(
#         models.Item.type == opposite_type,
#         models.Item.status == models.ItemStatus.open
#     ).all()

#     matches = []
#     for candidate in candidates:
#         distance = haversine(new_item.location_lat, new_item.location_lng,
#                              candidate.location_lat, candidate.location_lng)
#         if distance <= 5:  # Only consider matches within 5 km
#             score = compute_match_score(new_item, candidate)
#             if score >= 75:  # Only return good matches
#                 matches.append((score, candidate))

#     matches.sort(reverse=True, key=lambda x: x[0])
#     return [match[1] for match in matches]

@match_router.get("/found/{item_id}", response_model=MatchListResponse, status_code=200,
                 description="Get all lost items matched to a found item")
def get_lost_items_matched_to_found_item(
    item_id: UUID,
    db: Session = Depends(get_db)
):
    # Confirm this is a valid found item
    found_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not found_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if found_item.type != models.ItemType.found:
        raise HTTPException(status_code=400, detail="Item is not of type 'found'")

    # Get all matches where this item is the matched_item
    matches = (
        db.query(models.Match)
        .join(models.Item, models.Match.item_id == models.Item.id)
        .filter(models.Match.matched_item_id == item_id)
        .order_by(models.Match.score.desc())
        .all()
    )

    matches= [
        MatchedLostItem(
            match_score=match.score,
            lost_item=ItemOut.from_orm(match.item)  # `item` is the lost item
        )
        for match in matches
    ]
    return MatchListResponse(count=len(matches), items=matches)
