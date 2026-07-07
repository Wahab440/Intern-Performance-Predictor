from __future__ import annotations

import os
from functools import lru_cache

from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient | None:
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        return None

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1500)
        client.admin.command("ping")
        return client
    except Exception:
        return None


def get_predictions_collection():
    client = get_mongo_client()
    if client is None:
        return None

    database_name = os.getenv("MONGODB_DB", "intern_performance")
    collection_name = os.getenv("MONGODB_COLLECTION", "predictions")
    return client[database_name][collection_name]