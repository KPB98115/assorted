from fastapi.responses import StreamingResponse
from core.models.image import UploadImageParams, UploadImageResponse, DeleteImageParams, GetImageParams
from uuid import UUID

async def upload_image(params: UploadImageParams) -> UploadImageResponse:
    """
    Push upload process into threadpool queue
    Return: Job id of that process
    """
    # TODO: Convert image to webp in threadpool queue
    status = False
    # TODO: Upload image to disk in threadpool queue
    job_id = None
    return UploadImageResponse(status, job_id)

async def delete_image(params: DeleteImageParams) -> bool:
    return False

async def get_image(params: GetImageParams) -> StreamingResponse | None:
    return None

async def get_image_thumbnail(id: str) -> StreamingResponse | None:
    # TODO: If id not exist, check album_id and image_id,
    # if album and image exist, create a new thumbnail and return.
    # Otherwise return None
    return None