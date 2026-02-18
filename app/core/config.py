import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Inventory Location API"
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
