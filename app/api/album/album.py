from fastapi import APIRouter, HTTPException
from app.core.models.album import (
    AlbumCreateRequest,
    AlbumDeleteRequest,
    AlbumGetRequest,
    Album,
)
from app.core.helper.album import create_album, get_album, delete_album

router = APIRouter()

@router.post("/create")
async def create(name: AlbumCreateRequest) -> Album:
    return await create_album(name)

@router.post("/get")
async def get(id: AlbumGetRequest) -> Album:
    return await get_album(id)

@router.post("/delete")
async def delete(id: AlbumDeleteRequest) -> str:
    if await delete_album(id):
        return "Delete successfully"
    raise HTTPException(status_code=500, detail="Fail to delete album")