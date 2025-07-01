from quantiq.core.errors import BadRequestException


class AssetNotInsertedError(BadRequestException):
    def __init__(self, message: str = "Asset not inserted"):
        super().__init__(detail={"message": message})
