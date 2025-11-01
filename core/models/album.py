from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AlbumCreateRequest(BaseModel):
    name: str

class AlbumGetRequest(BaseModel):
    id: str

class AlbumDeleteRequest(BaseModel):
    id: str

class Album(BaseModel):
    id: UUID
    name: str
    create_date: datetime
    content: list[UUID]