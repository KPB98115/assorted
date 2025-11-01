from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import Annotated
from uuid import UUID

from core.models.image import AllowedImageFormat, UploadImageParams, DeleteImageParams, GetImageParams
from core.helper.image import upload_image, delete_image, get_image, get_image_thumbnail

router = APIRouter()

@router.post("/upload")
async def upload(album_id: Annotated[UUID, Form()], image: Annotated[UploadFile, File()]):
    if image.content_type not in AllowedImageFormat:
        raise HTTPException(status_code=400, detail=f"Unsupport file type: {image.content_type}")
    
    return await upload_image(UploadImageParams(album_id, image)) 

@router.post("delete")
async def delete(album_id: UUID, image_id: UUID):
    result = await delete_image(DeleteImageParams(album_id, image_id))
    if result is None:
        raise HTTPException(status_code=400, detail="Fail to delete image")
    return result

@router.post("/get")
async def get(album_id: UUID, image_id: UUID):
    result = await get_image(GetImageParams(album_id, image_id))
    if isinstance(result, StreamingResponse):
        return result
    raise HTTPException(status_code=400, detail="Fail to get image")

@router.post("/thumbnail/get")
async def get_thumbnail(thumbnail_id: str):
    result = await get_image_thumbnail(thumbnail_id)
    if isinstance(result, StreamingResponse):
        return result
    raise HTTPException(status_code=400, detail="Fail to get thumbnail")
