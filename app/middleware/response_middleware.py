from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json

DOC_PATHS = {"/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect"}

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.url.path in DOC_PATHS or request.url.path.startswith("/static"):
            return response

        if response.headers.get("content-type", "").startswith("application/json"):
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            try:
                original_content = json.loads(response_body.decode())
            except json.JSONDecodeError:
                original_content = response_body.decode()

            wrapped_content = {
                "status": response.status_code,
                "content": original_content
            }

            new_headers = dict(response.headers)
            new_headers.pop("content-length", None)

            return JSONResponse(
                content=wrapped_content,
                status_code=response.status_code,
                headers=new_headers
            )

        return response