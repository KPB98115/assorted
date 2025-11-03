from pydantic import BaseModel
from typing import Optional, Tuple
from datetime import datetime

class AlbumCreateRequest(BaseModel):
    name: str

class AlbumGetRequest(BaseModel):
    id: str

class AlbumDeleteRequest(BaseModel):
    id: str

class Album(BaseModel):
    _id: Optional[str] = None
    name: str
    create_date: datetime
    content: list[str]

class AlbumOperationResult(BaseModel):
    result: Optional[Tuple[bool, str]] = None