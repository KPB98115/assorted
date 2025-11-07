from pydantic import BaseModel
from fastapi import UploadFile

AllowedImageFormat = {"image/jpeg", "image/png", "image/webp", "image/heif", "image/heic", "image/avif"}

class UploadImageParams(BaseModel):
    album_id: str
    image: UploadFile

class UploadImageResponse(BaseModel):
    status: bool
    job_id: str

class DeleteImageParams(BaseModel):
    album_id: str
    image_id: str

class GetImageParams(BaseModel):
    album_id: str
    image_id: str

