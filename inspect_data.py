import os
from pymongo import MongoClient
from dotenv import load_dotenv
import pprint

load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client.get_database() # Should get 'test' from URI

print(f"Database: {db.name}")
print(f"Collections: {db.list_collection_names()}")

latest = db.readings.find_one(sort=[('timestamp', -1)])
print("\nLatest Reading:")
pprint.pprint(latest)

count = db.readings.count_documents({})
print(f"\nTotal Readings: {count}")
