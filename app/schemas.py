from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    ADJUSTMENT = "adjustment"

class ItemBase(BaseModel):
    sku: str
    name: str
    quantity_total: int = 0
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InventoryBase(BaseModel):
    item_id: int
    location_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    transaction_type: TransactionType = TransactionType.ADJUSTMENT
    notes: Optional[str] = None

class InventoryResponse(InventoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    item: Optional[ItemResponse] = None
    location: Optional[LocationResponse] = None
    
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    item_id: int
    location_id: int
    quantity_change: int
    transaction_type: TransactionType
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True