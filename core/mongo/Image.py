from fastapi import UploadFile
from core.models.image import Image
from core.mongo.mongo import BaseMongoClient
from gridfs import GridFS
from pymongo.errors import CollectionInvalid
import logging

logger = logging.getLogger(__name__)

class ImageClient(BaseMongoClient):
    def __init__(self):
        super().__init__(db_name="album", coll_name="image")

    async def init(self):
        """Initialize the image collection and GridFS bucket"""
        try:
            await self.database.create_collection("image", check_exists=True)
            await self.collection.create_index("name", unique=True)
        except CollectionInvalid as e:
            # Expected exception, ignore
            logger.info(f"'image' collection already exists. Skip the creation.")
        except Exception as e:
            # Other errors should be raised
            logger.error(f"Failed to create 'image' collection: {e}")
            raise

        # Initialize GridFS bucket
        self.init_bucket()
        logger.info("Initialized GridFS bucket for images")

    async def insertImageToBucket(image: UploadFile) -> bool:
        pass

    async def deleteImageFromBucket(image_id: str) -> bool:
        pass

    async def getImageById(id: str) -> Image:
        pass

    async def getImageByName(name: str) -> Image:
        pass