from core.mongo.mongo import BaseMongoClient
from pymongo.errors import CollectionInvalid
from typing import Optional
from bson import ObjectId
import logging
import os

logger = logging.getLogger(__name__)

class ImageClient(BaseMongoClient):
    def __init__(self):
        super().__init__(db_name="album", coll_name="image")

    async def init(self):
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

        self.init_bucket()
        logger.info("Initialized GridFS bucket for images")

    async def uploadFileToBucket(self, file_path: str, filename: str) -> str:
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            logger.info(f"Starting uploading {filename}")

            with open(file_path, 'rb') as f:
                file_id = await self.gridfs_bucket.upload_from_stream(
                    filename,
                    f,
                    metadata={"content_type": "image/webp"}
                )

            logger.info("Upload success")
            
            return str(file_id)
        except Exception as e:
            logger.error(f"Upload failed {filename}")
            raise

    async def getFileFromBucket(self, file_id: str):
        try:
            from bson import ObjectId
            logger.info(f"file id: {file_id}")

            grid_out = await self.gridfs_bucket.open_download_stream(ObjectId(file_id))

            contents = await grid_out.read()

            logger.info(f"Get File successfully: {file_id}")
            return contents

        except Exception as e:
            logger.info(e)
            return None

    async def deleteFileFromBucket(self, file_id: str) -> bool:
        try:
            await self.gridfs_bucket.delete(ObjectId(file_id))
            return True
        except Exception as e:
            logger.info(f"fail to delete file in bucket: {e}")
            return False

    async def findThumbnailByMainId(self, main_image_id: str) -> Optional[str]:
        try:
            cursor = self.gridfs_bucket.find({"filename": f"thumbnail_{main_image_id}.webp"})
            files = await cursor.to_list(length=1)
            if files:
                thumbnail_id = str(files[0]._id)
                logger.info(f"Thumbnail found: {thumbnail_id}")
                return thumbnail_id
            return None
        except Exception as e:
            logger.info(f"Failed to find thumbnail: {e}")
            return None