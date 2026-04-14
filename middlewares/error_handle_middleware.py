from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import logging

logger = logging.getLogger(__name__)

async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # log the full traceback
        logger.error(
            f"Unhandled error on {request.method} {request.url.path}\n"
            f"{traceback.format_exc()}"
        )
        # return clean error to client — never expose internals
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )