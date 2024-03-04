from pymongo import MongoClient 
from typing import Sequence

def get_client(host: str | Sequence[str] | None = None, port: int | None = None) -> MongoClient:
    return MongoClient(host, port)