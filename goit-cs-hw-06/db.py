from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")  # Для docker-compose
db = client["messages_db"]
collection = db["messages"]

def save_to_db(data):
    collection.insert_one(data)
