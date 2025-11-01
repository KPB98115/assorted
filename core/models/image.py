from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from fastapi import UploadFile

class Thumbnail(BaseModel):
    id: UUID

class Image(BaseModel):
    id: UUID
    name: str
    create_date: datetime
    thumbnail: Thumbnail

AllowedImageFormat = {"image/jpeg", "image/png", "image/webp", "image/heif", "image/heic", "image/avif"}

class UploadImageParams(BaseModel):
    album_id: UUID
    image: UploadFile

class UploadImageResponse(BaseModel):
    status: bool
    job_id: UUID

class DeleteImageParams(BaseModel):
    album_id: UUID
    image_id: UUID

class GetImageParams(BaseModel):
    album_id: UUID
    image_id: UUID

