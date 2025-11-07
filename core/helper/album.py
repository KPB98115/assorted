from fastapi import Request
from core.models.album import Album, AlbumCreateRequest, AlbumCreateResponse, AlbumGetRequest, AlbumDeleteRequest, AlbumOperationResult
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


async def create_album(album_data: AlbumCreateRequest, request: Request) -> Optional[AlbumCreateResponse]:
    logger.info(f"Create album request - name={album_data.name}")

    try:
        album_client = request.app.state.album_client
        result = await album_client.createAlbum(album_data.name)

        if not result.status:
            logger.warning(f"Failed to create album: {result.message}")
            return None

        album_id = result.message
        logger.info(f"Album created: {album_id}")

        return AlbumCreateResponse(album_id=album_id)

    except Exception as e:
        logger.error(f"Create album failed: {e}")
        return None

async def get_album(album_data: AlbumGetRequest, request: Request) -> Optional[Album]:
    try:
        album_client = request.app.state.album_client
        album = await album_client.getAlbumById(album_data.id)

        if album is None:
            logger.warning(f"Album not found")
            return None

        logger.info(f"Get album success: {album.id}")
        return album

    except Exception as e:
        logger.error(f"Get album failed: {e}")
        return None

async def get_all_album(request: Request) -> Optional[List[Album]]:
    try:
        album_client = request.app.state.album_client

        return await album_client.getAllAlbum() or None
    except Exception as e:
        return None

async def delete_album(album_data: AlbumDeleteRequest, request: Request) -> AlbumOperationResult:
    logger.info(f"Delete album request - album_id={album_data.id}")

    try:
        album_client = request.app.state.album_client
        image_client = request.app.state.image_client

        album = await album_client.getAlbumById(album_data.id)
        if album is None:
            logger.warning(f"Album not found")
            return AlbumOperationResult(status=False, message=f"Album not found")

        print(len(album.content))

        failed_deletions = []
        for image_pair in album.content:
            main_deleted = await image_client.deleteFileFromBucket(image_pair.image_id)
            if not main_deleted:
                failed_deletions.append(f"main:{image_pair.image_id}")

            thumb_deleted = await image_client.deleteFileFromBucket(image_pair.thumbnail_id)
            if not thumb_deleted:
                failed_deletions.append(f"thumb:{image_pair.thumbnail_id}")

        if failed_deletions:
            error_msg = f"Failed to delete some images: {', '.join(failed_deletions)}"
            return AlbumOperationResult(status=False, message=error_msg)

        # 3. Delete album from MongoDB
        result = await album_client.deleteAlbumByName(album.name)
        if not result.status:
            return AlbumOperationResult(status=False, message=f"Failed to delete album")

        logger.info(f"Album deleted success:{album_data.id}")
        return AlbumOperationResult(status=True, message=f"Album and images deleted successfully")

    except Exception as e:
        logger.error(f"Delete album failed: {e}")
        return AlbumOperationResult(status=False, message=f"Delete album failed: {str(e)}")

async def get_all_albums(request: Request) -> list[Album]:
    try:
        album_client = request.app.state.album_client

        albums = await album_client.getAllAlbums()

        return albums

    except Exception as e:
        logger.error(f"Get all albums failed: {e}")
        return []