from pymongo.asynchronous.mongo_client import AsyncMongoClient
from gridfs import AsyncGridFSBucket
from dotenv import load_dotenv
import os

load_dotenv()

class BaseMongoClient:
    def __init__(self, db_name: str, coll_name: str):
        self.uri = f"{os.getenv("MONGO_DB_HOST")}:{os.getenv("MONGO_DB_PORT")}"
        self.client = AsyncMongoClient(f"mongodb://{self.uri}")
        self.database = self.client.get_database(db_name)
        self.collection = self.database.get_collection(coll_name)
        self.gridfs_bucket = None

    def init_bucket(self):
        # TODO: Check if the bucket already exist, if not create one
        self.gridfs_bucket = AsyncGridFSBucket(self.database, bucket_name="image_bucket")
    
    async def close(self):
        await self.client.close()
