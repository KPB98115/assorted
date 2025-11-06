from fastapi import APIRouter, HTTPException, Request
from core.models.album import (
    AlbumCreateRequest,
    AlbumCreateResponse,
    AlbumDeleteRequest,
    AlbumGetRequest,
    AlbumOperationResult,
    Album,
)
from core.helper.album import create_album, get_album, delete_album, get_all_albums
from typing import List

router = APIRouter()

@router.post("/create")
async def create(request: Request, album_data: AlbumCreateRequest) -> AlbumCreateResponse:
    result = await create_album(album_data, request)
    if result is None:
        raise HTTPException(status_code=400, detail="Fail to create album: album name already exists.")
    return result

@router.post(f"/get")
async def get(request: Request, album_data: AlbumGetRequest) -> Album:
    result = await get_album(album_data, request)
    if result is None:
        raise HTTPException(status_code=500, detail="Fail to get album")
    return result

@router.post("/getAll")
async def getAll(request: Request) -> List[Album]:
    result = await get_all_albums(request)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to get all albums")
    return result

@router.post("/delete")
async def delete(request: Request, album_data: AlbumDeleteRequest) -> AlbumOperationResult:
    result = await delete_album(album_data, request)
    if not result.status:
        raise HTTPException(status_code=500, detail=f"Fail to delete album: {result.message}")
    return result