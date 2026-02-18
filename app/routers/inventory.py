from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud
from ..db import get_db
from .. import deps

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(deps.get_current_active_user)]
)

@router.post("/movement", response_model=schemas.InventoryResponse)
def create_inventory_movement(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    # Verify item exists and is active
    db_item = crud.get_item(db, item_id=inventory.item_id)
    if not db_item or not db_item.is_active:
        raise HTTPException(status_code=404, detail="Item not found or inactive")
        
    # Verify location exists and is active
    db_location = crud.get_location(db, location_id=inventory.location_id)
    if not db_location or not db_location.is_active:
         raise HTTPException(status_code=404, detail="Location not found or inactive")

    # Perform movement
    return crud.create_inventory_movement(db=db, inventory=inventory)

@router.get("/", response_model=List[schemas.InventoryResponse])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventory = crud.get_inventories(db, skip=skip, limit=limit)
    return inventory

@router.get("/transactions", response_model=List[schemas.TransactionResponse])
def read_transactions(
    skip: int = 0, 
    limit: int = 100, 
    item_id: Optional[int] = Query(None, description="Filter by Item ID"),
    location_id: Optional[int] = Query(None, description="Filter by Location ID"),
    db: Session = Depends(get_db)
):
    transactions = crud.get_transactions(db, skip=skip, limit=limit, item_id=item_id, location_id=location_id)
    return transactions
