from fastapi import FastAPI
from app import models
from app.db import engine
from app.routers import items, locations, inventory

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(locations.router)
app.include_router(inventory.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Location API"}
