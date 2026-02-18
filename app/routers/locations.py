from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..db import get_db
from .. import deps

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(deps.get_current_active_user)]
)

@router.post("/", response_model=schemas.LocationResponse)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_name(db, name=location.name)
    if db_location:
        raise HTTPException(status_code=400, detail="Location already registered")
    return crud.create_location(db=db, location=location)

@router.get("/", response_model=List[schemas.LocationResponse])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations

@router.get("/{location_id}", response_model=schemas.LocationResponse)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.delete("/{location_id}", response_model=schemas.LocationResponse)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location(db, location_id=location_id)
    if not db_location:
         raise HTTPException(status_code=404, detail="Location not found")
    return crud.soft_delete_location(db=db, location_id=location_id)
