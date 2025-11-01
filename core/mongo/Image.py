from fastapi import UploadFile
from core.models.image import Image
from core.mongo.mongo import BaseMongoClient
from gridfs import GridFS

class ImageClient(BaseMongoClient):
    def __init__(self):
        super().__init__(db_name="album", coll_name="album")

    async def insertImageToBucket(image: UploadFile) -> bool:
        pass
    
    async def getImageById(id: str) -> Image:
        pass