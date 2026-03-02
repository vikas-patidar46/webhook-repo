from flask_pymongo import PyMongo
from pymongo import MongoClient

# Setup MongoDB here
# mongo = PyMongo(uri="mongodb://localhost:27017/database")
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["github_events"]
events_collection = db["events"]


