from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.middleware.error_middleware import ErrorMiddleware
from app.middleware.response_middleware import ResponseMiddleware
from starlette.responses import RedirectResponse
from app.api import router as api_router
from core.mongo.Album import AlbumClient
from core.mongo.Image import ImageClient

app = FastAPI()

app.add_middleware(ErrorMiddleware)
app.add_middleware(ResponseMiddleware)

app.include_router(api_router, prefix="/api")

@asynccontextmanager
async def initMongoDB(app: FastAPI):
    app.state.album_client = AlbumClient()
    await app.state.album_client.init()

    app.state.image_client = ImageClient()
    await app.state.image_client.init()

    yield
    
    await app.state.album_client.close()
    await app.state.image_client.close()

@app.get("/")
async def read_root():
    return RedirectResponse(url="/health")

@app.get("/health")
async def health_check():
    return {"status": "ok"}