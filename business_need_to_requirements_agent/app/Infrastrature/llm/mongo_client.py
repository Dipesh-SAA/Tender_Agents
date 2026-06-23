import os

from dotenv import load_dotenv
from pymongo import MongoClient
 
load_dotenv()


def _get_database():
    mongo_uri = os.getenv("MONGODB_URI")
    mongo_database = os.getenv("MONGODB_DATABASE")

    missing_settings = [
        name
        for name, value in {
            "MONGODB_URI": mongo_uri,
            "MONGODB_DATABASE": mongo_database,
        }.items()
        if not value
    ]

    if missing_settings:
        raise ValueError(
            "Missing required MongoDB environment variable(s): "
            + ", ".join(missing_settings)
        )

    client = MongoClient(mongo_uri)
    return client[mongo_database]


def get_document(collection_name, filter_query):
    db = _get_database()
    collection = db[collection_name]
    return collection.find_one(filter_query)
