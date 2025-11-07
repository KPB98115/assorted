from datetime import datetime
from typing import Optional

from bson import ObjectId
from core.models.album import Album, AlbumOperationResult, ImagePair
from core.mongo.mongo import BaseMongoClient
from pymongo.errors import CollectionInvalid
from typing import List
import logging

logger = logging.getLogger(__name__)

class AlbumClient(BaseMongoClient):
    def __init__(self):
        super().__init__(db_name="album", coll_name="album")

    async def init(self):
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
                return AlbumOperationResult(status=False, message="Album already exist")

            album = Album(
                _id=None,
                name=name,
                create_date=datetime.now(),
                content=[]
            )
            record = await self.collection.insert_one(album.model_dump())
            return AlbumOperationResult(status=True, message=str(record.inserted_id))
        except Exception as e:
            return AlbumOperationResult(status=False, message=str(e))

    async def deleteAlbumByName(self, name: str) -> AlbumOperationResult:
        try:
            if not await self.getAlbumByName(name):
                return AlbumOperationResult(status=False, message="Album name does not exist.")

            await self.collection.delete_one({"name": name})
            return AlbumOperationResult(status=True, message="Album delete successfully.")
        except Exception as e:
            return AlbumOperationResult(status=False, message=str(e))
    async def addImageToAlbum(self, album_id: str, image_id: str, thumbnail_id: str) -> AlbumOperationResult:
        try:
            album = await self.getAlbumById(album_id)
            if album is None:
                return AlbumOperationResult(status=False, message=f"Fail to access album: {album_id} not exist.")

            # Check if image already exists in album
            if any(pair.image_id == image_id for pair in album.content):
                return AlbumOperationResult(status=False, message="Image already in album.")

            image_pair = ImagePair(image_id=image_id, thumbnail_id=thumbnail_id)
            await self.collection.update_one(
                {"_id": ObjectId(album_id)},
                {"$push": {
                    "content": image_pair.model_dump()
                }})
            return AlbumOperationResult(status=True, message=f"Image {image_id} added to album successfully.")
        except Exception as e:
            return AlbumOperationResult(status=False, message=str(e))

    async def deleteImageFromAlbum(self, album_id: str, image_id: str) -> AlbumOperationResult:
        try:
            album = await self.getAlbumById(album_id)
            if album is None:
                return AlbumOperationResult(status=False, message=f"Fail to access album: {album_id} is not exist.")

            # Check if image exists in album
            if not any(pair.image_id == image_id for pair in album.content):
                return AlbumOperationResult(status=False, message="Image not in album.")

            await self.collection.update_one(
                {"_id": ObjectId(album_id)},
                {"$pull": {
                    "content": {"image_id": image_id}
                }}
            )
            return AlbumOperationResult(status=True, message="Delete image from album successfully.")
        except Exception as e:
            return AlbumOperationResult(status=False, message=str(e))

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

    async def getAllAlbums(self) -> List[Album]:
        albums = []
        cursor = self.collection.find({})
        async for album_doc in cursor:
            albums.append(Album(**album_doc))
        return albums