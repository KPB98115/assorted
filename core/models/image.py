from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile

class Thumbnail(BaseModel):
    _id: str

class Image(BaseModel):
    _id: Optional[str] = None
    name: str
    create_date: datetime
    thumbnail: Thumbnail

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

