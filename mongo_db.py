import os

from pymongo import MongoClient


class MongoDB:
    def __init__(self, host=f'mongodb+srv://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}',
                 db_name='self-bot'):
        self.client = MongoClient(host)
        self.db = self.client[db_name]

    def insert(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_one(data)

    def find(self, collection_name, query=None):
        collection = self.db[collection_name]
        return collection.find(query or {})
