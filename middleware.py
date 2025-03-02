from fastapi import Request
from logger import logger


async def log_req(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        raise
    else:
        logger.info(f"Outgoing response: {response.status_code}")
        return response
