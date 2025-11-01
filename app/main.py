from fastapi import FastAPI
from app.middleware.error_middleware import ErrorMiddleware
from app.middleware.response_middleware import ResponseMiddleware
from starlette.responses import RedirectResponse
from app.api import router as api_router

app = FastAPI()

app.add_middleware(ErrorMiddleware)
app.add_middleware(ResponseMiddleware)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    return RedirectResponse(url="/health")

@app.get("/health")
async def health_check():
    return {"status": "ok"}