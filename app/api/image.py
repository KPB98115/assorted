from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import Annotated

from core.models.image import AllowedImageFormat, UploadImageParams, DeleteImageParams, GetImageParams, GetThumbnailParams
from core.helper.image import upload_image, delete_image, get_image, get_thumbnail
from core.helper.converter import Job

router = APIRouter()

@router.post("/upload")
async def upload(request: Request, album_id: Annotated[str, Form()], image: Annotated[UploadFile, File()]):
    if image.content_type not in AllowedImageFormat:
        raise HTTPException(status_code=400, detail=f"Unsupport file type: {image.content_type}")

    return await upload_image(UploadImageParams(album_id=album_id, image=image), request)

@router.post("/delete")
async def delete(request: Request, params: DeleteImageParams):
    result = await delete_image(params, request)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to delete image")
    return {"message": "Image deleted successfully"}

@router.post("/get")
async def get(request: Request, params: GetImageParams):
    result = await get_image(params, request)
    if isinstance(result, StreamingResponse):
        return result
    raise HTTPException(status_code=404, detail="Image not found")

@router.post("/thumbnail/get")
async def get_thumbnail_endpoint(request: Request, params: GetThumbnailParams):
    result = await get_thumbnail(params.thumbnail_id, request)
    if isinstance(result, StreamingResponse):
        return result
    raise HTTPException(status_code=404, detail="Thumbnail not found")

@router.get("/job/{job_id}")
async def get_job_status(request: Request, job_id: str):
    """Get the status of an image conversion job"""
    converter = request.app.state.converter
    job: Job = converter.getJob(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    response = {
        "job_id": job.id,
        "overall_status": job.status.name,
        "main_image": {
            "status": job.main_image.status.name,
            "gridfs_id": job.main_image.gridfs_id,
            "error_message": job.main_image.error_message
        },
        "thumbnail": {
            "status": job.thumbnail.status.name,
            "gridfs_id": job.thumbnail.gridfs_id,
            "error_message": job.thumbnail.error_message
        },
        "album_association": {
            "associated": job.album_association.associated if job.album_association else False,
            "error_message": job.album_association.error_message if job.album_association else None
        } if job.album_association else None
    }

    return response

@router.delete("/job/{job_id}")
async def delete_job(request: Request, job_id: str):
    """Delete a job from memory (useful after retrieving results)"""
    converter = request.app.state.converter
    success = converter.delete_job(job_id)

    if not success:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"message": "Job deleted successfully"}
