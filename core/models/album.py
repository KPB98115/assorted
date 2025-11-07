from pydantic import BaseModel
from typing import Optional, Tuple
from datetime import datetime

class AlbumCreateRequest(BaseModel):
    name: str

class AlbumCreateResponse(BaseModel):
    album_id: str

class AlbumGetRequest(BaseModel):
    id: str

class AlbumDeleteRequest(BaseModel):
    id: str

class ImagePair(BaseModel):
    image_id: str
    thumbnail_id: str

class Album(BaseModel):
    _id: Optional[str] = None
    name: str
    create_date: datetime
    content: list[ImagePair]

class AlbumOperationResult(BaseModel):
    status: bool
    message: str