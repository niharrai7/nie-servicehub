import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "NIE ServiceHub API")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    PORT: int = int(os.getenv("PORT", os.getenv("APP_PORT", "8000")))
    
    # Support both MONGO_URI and MONGODB_URI
    MONGO_URI: str = os.getenv("MONGODB_URI", os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    MONGO_DB_NAME: str = os.getenv("MONGODB_DATABASE", os.getenv("MONGO_DB_NAME", "nie_servicehub"))

settings = Settings()
