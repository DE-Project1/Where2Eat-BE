from pymongo import MongoClient
from src.core.config import settings

client = MongoClient(settings.mongo_uri)
db = client[settings.mongo_db]
