import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import settings

logger = logging.getLogger("nie_servicehub.database")

class Database:
    client: MongoClient = None
    db = None

db_instance = Database()

def get_database():
    if db_instance.client is None:
        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGO_URI}...")
            db_instance.client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            # The ismaster command is cheap and does not require auth.
            db_instance.client.admin.command('ismaster')
            db_instance.db = db_instance.client[settings.MONGO_DB_NAME]
            logger.info(f"Successfully connected to MongoDB database: '{settings.MONGO_DB_NAME}'")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e
    return db_instance.db

def close_database():
    if db_instance.client:
        db_instance.client.close()
        db_instance.client = None
        logger.info("MongoDB connection closed.")
