from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Form, Path, Query, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.lost_found.models import Item, ItemStatus, ItemType, Match
from app.lost_found.schema import ItemListResponse, ItemOut
from typing import Optional
from app.utils.matching import compute_match_score
from app.utils.minio import upload_to_minio

router = APIRouter(prefix='/item',tags=["lost_found"])

@router.post("/", response_model=ItemOut, description="Create a new lost or found item", status_code=201, name="Create an Item")
def create_item(
    title: str = Form(...),
    description: str = Form(...),
    location_lat: str = Form(...),
    location_lng: str = Form(...),
    contact_email: str = Form(...),
    contact_name: str = Form(...),
    type: ItemType = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Upload image if provided
    image_url = upload_to_minio(image) if image else None

    # Create item in DB
    db_item = Item(
        id=uuid4(),
        title=title,
        description=description,
        location_lat=location_lat,
        location_lng=location_lng,
        contact_email=contact_email,
        contact_name=contact_name,
        type=type,
        status=ItemStatus.open,
        image_url=image_url
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Auto match if item is LOST
    if db_item.type == ItemType.lost:
        candidates = db.query(Item).filter(
            Item.type == ItemType.found,
            Item.status == ItemStatus.open
        ).all()

        for found_item in candidates:
            score = compute_match_score(db_item, found_item)
            if score > 50:
                match = Match(
                    item_id=db_item.id,
                    matched_item_id=found_item.id,
                    score=score
                )
                db.add(match)

        db.commit()

    return db_item


@router.get("/", response_model=ItemListResponse, description="List all items", status_code=200, name="List all Items")
def list_items(
    type: Optional[ItemType] = Query(None),
    status: Optional[ItemStatus] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Item)
    
    if type:
        query = query.filter(Item.type == type)
    if status:
        query = query.filter(Item.status == status)
    
    items = query.order_by(Item.timestamp.desc()).all()
    return ItemListResponse(count=len(items), items=items)


@router.get("/{item_id}", response_model=ItemOut, description="Get item by ID", status_code=200)
def get_item_by_id(item_id: UUID, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}/status", description="Update item status", status_code=200)
def update_item_status(
    item_id: UUID = Path(..., description="UUID of the item"),
    new_status: ItemStatus = ItemStatus.resolved,
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status = new_status
    db.commit()
    db.refresh(item)

    return {"message": f"Item {item_id} status updated to '{new_status}'."}
