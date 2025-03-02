from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from logger import logger


async def exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}", exc_info=True)

    return JSONResponse(
        status_code=exc.status_code, content={
            "message": exc.detail})
