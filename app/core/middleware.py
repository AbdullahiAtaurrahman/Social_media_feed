import time, uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        response = await call_next(request)

        duration = (time.perf_counter() - start) * 1000  # ms
        response.headers["X-Process-Time"] = f"{duration:.2f}ms"
        response.headers["X-Request-ID"] = request_id
        return response
