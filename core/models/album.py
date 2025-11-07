from pydantic import BaseModel, ConfigDict, Field
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
    model_config = ConfigDict(populate_by_name=True, json_encoders={datetime: lambda v: v.isoformat()})

    id: Optional[str] = Field(None, alias="_id", serialization_alias="id")
    name: str
    create_date: datetime
    content: list[ImagePair]

class AlbumOperationResult(BaseModel):
    status: bool
    message: str