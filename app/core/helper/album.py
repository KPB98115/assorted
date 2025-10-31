from fastapi import Request
from app.core.models.album import Album
import uuid
from datetime import datetime


async def create_album(name: str) -> Album:
    # TODO Check if album name already exists
    # If exists, return album already exists error
    album = Album(
        id=str(uuid.uuid4()),
        name=name,
        create_date=datetime.now(),
        content=[]
    )
    
    # TODO: Save album metadata to database
    
    return album

async def get_album(id: str) -> Album:
    # TODO: check if album id is not exist
    # If not exist, return album not exist error

    # TODO: Get album metadata from database
    pass

async def delete_album(id: str) -> bool:
    # TODO: check if album id is not exist
    # If so, return True
    # Otherwise, delete the album and delete the images recursively
    return True