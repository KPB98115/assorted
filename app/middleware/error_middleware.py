from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)

            if response.status_code >= 400:
                response_body = b""
                async for chunk in response.body_iterator:
                    response_body += chunk

                try:
                    original_content = json.loads(response_body.decode())
                    if isinstance(original_content, dict):
                        message = original_content.get("detail") or original_content.get("message") or str(original_content)
                    else:
                        message = str(original_content)
                except:
                    message = response_body.decode() if response_body else "Error"

                # error_response = {
                #     "error_code": response.status_code,
                #     "message": message
                # }

                new_headers = dict(response.headers)
                new_headers.pop("content-length", None)

                return JSONResponse(
                    content=message,
                    status_code=response.status_code,
                    headers=new_headers
                )

            return response

        except Exception as e:
            error_response = {
                "error_code": 500,
                "message": str(e)
            }

            return JSONResponse(
                content=error_response,
                status_code=500
            )