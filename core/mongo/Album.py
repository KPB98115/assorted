from core.models.album import Album
from core.mongo.mongo import BaseMongoClient

class AlbumClient(BaseMongoClient):
    def __init__(self):
        super().__init__(db_name="album", coll_name="album")

    async def createAlbum(id: str) -> bool:
        pass

    async def deleteAlbumById(id: str) -> bool:
        pass

    async def getAlbumById(id: str) -> Album:
        pass

    async def addImageToAlbum(album_id: str, image_id: str) -> bool:
        pass

    async def removeImageFromAlbum(album_id: str, image_id: str) -> bool:
        pass

