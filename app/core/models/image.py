from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Thumbnail(BaseModel):
    id: UUID

class Image(BaseModel):
    id: UUID
    name: str
    create_date: datetime
    thumbnail: Thumbnail

