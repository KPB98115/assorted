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
    result = await create_album(name)
    if result is None:
        raise HTTPException(status_code=500, detail="Fail to create album: album name exist.")

@router.post("/get")
async def get(id: AlbumGetRequest) -> Album:
    result = await get_album(id)
    if result is None:
        raise HTTPException(status_code=500, detail="Fail to get album")

@router.post("/delete")
async def delete(id: AlbumDeleteRequest) -> str:
    if await delete_album(id):
        return "Delete successfully"
    raise HTTPException(status_code=500, detail="Fail to delete album")