from pymongo import MongoClient
from app.config import MONGO_URL

client = MongoClient(MONGO_URL)
master_db = client["master_db"]
org_collection = master_db["organizations"]
admin_collection = master_db["admins"]

def get_org_db(org_collection_name: str):
    return client["orgs"][org_collection_name]
