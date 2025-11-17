from fastapi import Request
from loguru import logger
from fastapi.responses import JSONResponse
from typing import Callable


class HandlerException(Exception):
    """base exception class"""

    def __init__(self, message: str = "Service is unavailable"):
        self.message = message
        super().__init__(self.message)


class UsernameAlreadyExists(HandlerException):
    """raise when username already exists"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, HandlerException], JSONResponse]:
    detail = {"message": initial_detail}

    async def exception_handler(_: Request, exc: HandlerException) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message

            logger.error(exc)
            return JSONResponse(
                status_code=status_code, content={"detail": detail["message"]}
            )

    return exception_handler
