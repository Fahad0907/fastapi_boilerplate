import time
import uuid
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next):
    # generate unique ID for each request — useful for tracing
    request_id = str(uuid.uuid4())[:8]

    logger.info(
        f"[{request_id}] "
        f"{request.method} {request.url.path} "
        f"| IP: {request.client.host}"
    )

    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    logger.info(
        f"[{request_id}] "
        f"Status: {response.status_code} "
        f"| Duration: {duration:.4f}s"
    )

    # attach request_id to response header — useful for debugging
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(round(duration * 1000, 2)) + "ms"

    return response