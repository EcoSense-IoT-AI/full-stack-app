import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")
print(f"URI: {uri}")

try:
    client = MongoClient(uri)
    db = client['test']
    print("Collections in 'test':", db.list_collection_names())
except Exception as e:
    print(f"Error: {e}")
