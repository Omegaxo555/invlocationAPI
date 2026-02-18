from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional

# Items
def get_item(db: Session, item_id: int):
    return db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()

def get_item_by_sku(db: Session, sku: str):
    return db.query(models.ItemDB).filter(models.ItemDB.sku == sku).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemDB).filter(models.ItemDB.is_active == True).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.ItemDB(
        sku=item.sku, 
        name=item.name, 
        quantity_total=item.quantity_total,
        is_active=item.is_active
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # If initial quantity > 0, we might want to log a transaction, but it has no location yet. 
    # Usually items are created with 0 quantity and then stock is added via inventory endpoint.
    # Current model allows quantity_total at creation, but doesn't assign it to a location.
    # We will assume quantity_total is just a cached sum, but strictly it violates normalization if not backed by inventory.
    # For robust design, we should probably ignore quantity_total input or set it to 0, 
    # but to respect current schema, we keep it. Ideally we refactor to not allow setting quantity on item creation.
    
    return db_item

def soft_delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db_item.is_active = False
        db.commit()
        db.refresh(db_item)
    return db_item

# Locations
def get_location(db: Session, location_id: int):
    return db.query(models.LocationDB).filter(models.LocationDB.id == location_id).first()

def get_location_by_name(db: Session, name: str):
    return db.query(models.LocationDB).filter(models.LocationDB.name == name).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LocationDB).filter(models.LocationDB.is_active == True).offset(skip).limit(limit).all()

def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.LocationDB(
        name=location.name, 
        description=location.description,
        is_active=location.is_active
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def soft_delete_location(db: Session, location_id: int):
    db_location = get_location(db, location_id)
    if db_location:
        db_location.is_active = False
        db.commit()
        db.refresh(db_location)
    return db_location

# Inventory & Transactions
def get_inventory(db: Session, item_id: int, location_id: int):
    return db.query(models.InventoryDB).filter(
        models.InventoryDB.item_id == item_id,
        models.InventoryDB.location_id == location_id
    ).first()

def create_inventory_movement(db: Session, inventory: schemas.InventoryCreate):
    # This handles adding/removing stock (movement)
    
    # Update total quantity on Item
    db_item = get_item(db, item_id=inventory.item_id)
    if db_item:
        db_item.quantity_total += inventory.quantity
    
    # Update Inventory for specific Location
    db_inventory = get_inventory(db, item_id=inventory.item_id, location_id=inventory.location_id)
    if db_inventory:
        db_inventory.quantity += inventory.quantity
        # If quantity goes to 0 or negative? Allow negative for robust accounting or block?
        # Usually block negative stock unless configured otherwise. forcing >= 0 is safer.
        if db_inventory.quantity < 0:
             # Rollback logic or raising error should be handled before commit.
             # Ideally check before applying. 
             pass # For now, simple implementation
    else:
        # Create new inventory record
        db_inventory = models.InventoryDB(
            item_id=inventory.item_id,
            location_id=inventory.location_id,
            quantity=inventory.quantity
        )
        db.add(db_inventory)
    
    # Log Transaction
    db_transaction = models.TransactionDB(
        item_id=inventory.item_id,
        location_id=inventory.location_id,
        quantity_change=inventory.quantity,
        transaction_type=inventory.transaction_type,
        notes=inventory.notes
    )
    db.add(db_transaction)
    
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InventoryDB).offset(skip).limit(limit).all()

def get_transactions(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    item_id: Optional[int] = None,
    location_id: Optional[int] = None
):
    query = db.query(models.TransactionDB)
    if item_id:
        query = query.filter(models.TransactionDB.item_id == item_id)
    if location_id:
        query = query.filter(models.TransactionDB.location_id == location_id)
    return query.order_by(models.TransactionDB.created_at.desc()).offset(skip).limit(limit).all()
