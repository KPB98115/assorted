from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.error_middleware import ErrorMiddleware
from app.middleware.response_middleware import ResponseMiddleware
from starlette.responses import RedirectResponse
from app.api import router as api_router
from core.mongo.Album import AlbumClient
from core.mongo.Image import ImageClient
from core.helper.converter import Converter
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.album_client = AlbumClient()
    await app.state.album_client.init()

    app.state.image_client = ImageClient()
    await app.state.image_client.init()

    main_loop = asyncio.get_running_loop()
    app.state.converter = Converter(
        image_client=app.state.image_client,
        main_event_loop=main_loop
    )

    yield

    # Cleanup
    app.state.converter.shutdown()
    await app.state.album_client.close()
    await app.state.image_client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(ErrorMiddleware)
app.add_middleware(ResponseMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    return RedirectResponse(url="/health")

@app.get("/health")
async def health_check():
    return {"status": "ok"}