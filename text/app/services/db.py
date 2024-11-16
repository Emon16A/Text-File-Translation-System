from pymongo import MongoClient
import os

# Connection URL from environment variable
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://emon:emon16@text.2ryp7.mongodb.net/?retryWrites=true&w=majority&appName=Text")

client = MongoClient(MONGO_URL)
db = client['translation_db']  # Your database name

def get_db():
    return db
