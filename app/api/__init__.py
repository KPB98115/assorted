from fastapi import APIRouter
from app.api.album.album import router as album_router
from app.api.image.image import router as image_router

router = APIRouter()

router.include_router(
    album_router,
    prefix="/album",
    tags=["album"]
)
router.include_router(
    image_router,
    prefix="/image",
    tags=["image"]
)