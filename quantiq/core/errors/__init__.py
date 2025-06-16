from fastapi import HTTPException

__all__ = ["NotFoundException", "BadRequestException"]
__version__ = "0.1.0"


class NotFoundException(HTTPException):
    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=404, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=400, detail=detail)
