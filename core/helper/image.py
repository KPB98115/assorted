from fastapi.responses import StreamingResponse
from core.models.image import UploadImageParams, UploadImageResponse, DeleteImageParams, GetImageParams
from fastapi import Request
import os
import uuid
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

async def upload_image(params: UploadImageParams, request: Request) -> UploadImageResponse:
    try:
        converter = request.app.state.converter
        album_client = request.app.state.album_client
        logger.info(f"Converter and album_client retrieved from app state")

        temp_filename = f"{uuid.uuid4().hex}_{params.image.filename}"
        temp_path = f"/tmp/{temp_filename}"

        logger.info(f"{temp_path}")
        with open(temp_path, "wb") as f:
            content = await params.image.read()
            f.write(content)

        job_id = converter.submit(temp_path, params.image.filename or "image", params.album_id, album_client)

        logger.info(f"Upload complete: {job_id}")
        return UploadImageResponse(status=True, job_id=job_id)

    except Exception as e:
        logger.error(f"Upload failed:{e}")
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        raise e

async def delete_image(params: DeleteImageParams, request: Request) -> bool:
    try:
        album_client = request.app.state.album_client
        image_client = request.app.state.image_client

        album = await album_client.getAlbumById(str(params.album_id))
        if album is None:
            logger.warning(f"Album not found")
            return False

        image_pair = next((pair for pair in album.content if pair.image_id == params.image_id), None)
        if image_pair is None:
            logger.warning(f"Image not in album")
            return False

        result = await album_client.deleteImageFromAlbum(str(params.album_id), params.image_id)

        if not result.status:
            logger.warning(f"Failed to remove image: {result.message}")
            return False

        main_deleted = await image_client.deleteFileFromBucket(params.image_id)

        if not main_deleted:
            logger.warning(f"Failed to delete main image")

        thumb_deleted = await image_client.deleteFileFromBucket(image_pair.thumbnail_id)
        if not thumb_deleted:
            logger.warning(f"Failed to delete thumbnail: {image_pair.thumbnail_id}")

        return True
    except Exception as e:
        logger.error(f"Delete image failed: {e}")
        return False

async def get_image(params: GetImageParams, request: Request) -> StreamingResponse | None:
    try: 
        album_client = request.app.state.album_client
        image_client = request.app.state.image_client

        album = await album_client.getAlbumById(str(params.album_id))
        if album is None:
            logger.warning(f"Album not found")
            return None

        if not any(pair.image_id == params.image_id for pair in album.content):
            logger.warning(f"Image not in album")
            return None

        contents = await image_client.getFileFromBucket(params.image_id)

        if contents is not None:
            return StreamingResponse(
                BytesIO(contents),
                media_type="image/webp",
                headers={"Content-Disposition": f"inline; filename=image_{params.image_id}.webp"}
            )
        return None

    except Exception as e:
        logger.error(f"Get image failed: {e}")
        return None

async def get_thumbnail(id: str, request: Request) -> StreamingResponse | None:
    try:
        image_client = request.app.state.image_client

        contents = await image_client.getFileFromBucket(id)

        if contents is not  None:
            return StreamingResponse(
                BytesIO(contents),
                media_type="image/webp",
                headers={"Content-Disposition": f"inline; filename=thumbnail_{id}.webp"}
            )
        return None
    except Exception as e:
        logger.error(f"Get thumbnail failed: {e}")
        return None