from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base
import enum

class TransactionType(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    ADJUSTMENT = "adjustment"

class TimestampMixin(object):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class ItemDB(Base, TimestampMixin):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    quantity_total = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    inventories = relationship("InventoryDB", back_populates="item")
    transactions = relationship("TransactionDB", back_populates="item")

class LocationDB(Base, TimestampMixin):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    inventories = relationship("InventoryDB", back_populates="location")
    transactions = relationship("TransactionDB", back_populates="location")

class InventoryDB(Base, TimestampMixin):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    quantity = Column(Integer, default=0)

    item = relationship("ItemDB", back_populates="inventories")
    location = relationship("LocationDB", back_populates="inventories")

class TransactionDB(Base, TimestampMixin):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    quantity_change = Column(Integer)
    transaction_type = Column(Enum(TransactionType), default=TransactionType.ADJUSTMENT)
    notes = Column(String, nullable=True)

    item = relationship("ItemDB", back_populates="transactions")
    location = relationship("LocationDB", back_populates="transactions")
