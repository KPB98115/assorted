from datetime import datetime
from typing import Optional

from bson import ObjectId
from core.models.album import Album, AlbumOperationResult
from core.models.image import Thumbnail
from core.mongo.mongo import BaseMongoClient
from pymongo.errors import CollectionInvalid
import logging

logger = logging.getLogger(__name__)

class AlbumClient(BaseMongoClient):
    def __init__(self):
        super().__init__(db_name="album", coll_name="album")

    async def init(self):
        """Initialize the album collection"""
        try:
            await self.database.create_collection("album", check_exists=True)
            await self.collection.create_index("name", unique=True)
        except CollectionInvalid as e:
            # Expected exception, ignore it
            logger.info(f"'album' collection already exists. Skip the createion.")
        except Exception as e:
            # Other errors should be raised
            logger.error(f"Failed to create 'album' collection: {e}")
            raise

    async def createAlbum(self, name: str) -> AlbumOperationResult:
        try:
            if await self.collection.find_one({"name": name}):
                return AlbumOperationResult((False, "Album already exist"))
            
            album = Album(
                _id=None,
                name=name,
                create_date=datetime.now(),
                content=[]
            )
            record = await self.collection.insert_one(album.model_dump())
            return AlbumOperationResult((True, str(record.inserted_id)))
        except Exception as e:
            return AlbumOperationResult((False, str(e)))

    async def deleteAlbumByName(self, name: str) -> AlbumOperationResult:
        try:
            if not await self.getAlbumByName(name):
                return AlbumOperationResult((False, "Album name does not exist."))
            
            await self.collection.delete_one({"name": name})
            return AlbumOperationResult((True, "Album delete successfully."))
        except Exception as e:
            return AlbumOperationResult((False, str(e)))
    async def addImageToAlbum(self, album_id: str, image_id: str) -> AlbumOperationResult:
        try:
            album = await self.getAlbumById(album_id)
            if album is None:
                return AlbumOperationResult((False, f"Fail to access album: {album_id} not exist."))
            if image_id in album.content:
                return AlbumOperationResult((False, "Image already in album."))
            
            await self.collection.update_one(
                {"_id": ObjectId(album_id)},
                {"$push": {
                    "content": image_id
                }})
            thumbnail_id = Thumbnail(_id=f"{album_id}_{image_id}").id
            return AlbumOperationResult((True, thumbnail_id))
        except Exception as e:
            return AlbumOperationResult((False, str(e)))

    async def deleteImageFromAlbum(self, album_id: str, image_id: str) -> AlbumOperationResult:
        try:
            album = await self.getAlbumById(album_id)
            if album is None:
                return AlbumOperationResult((False, f"Fail to access album: {album_id} is not exist."))
            if image_id not in album.content:
                return AlbumOperationResult((False, "Image not in album."))
            
            await self.collection.update_one(
                {"_id": ObjectId(album_id)},
                {"$pull": {
                    "content": image_id
                }}
            )
            return AlbumOperationResult((True, "Delete image from album successfully."))
        except Exception as e:
            return AlbumOperationResult((False, str(e)))

    # async def findAlbumById(self, id: str) -> Optional[Album]:
    #     album = await self.collection.find_one({"_id": ObjectId(id)})
    #     if album:
    #         return Album(**album)
    #     return None

    # async def findAlbumByName(self, name: str) -> Optional[Album]:
    #     album = await self.collection.find_one({"name": name})
    #     if album:
    #         return Album(**album)
    #     return None

    async def getAlbumById(self, id: str) -> Optional[Album]:
        album = await self.collection.find_one({"_id": ObjectId(id)})
        if album:
            return Album(**album)
        return None

    async def getAlbumByName(self, name: str) -> Optional[Album]:
        album = await self.collection.find_one({"name": name})
        if album:
            return Album(**album)
        return None
