from fastapi import APIRouter

from quantiq.modules.assets.services.asset_service import AssetService


class AssetController:
    def __init__(self, service: AssetService):
        self.router = APIRouter(prefix="/assets", tags=["assets"])
        self.service = service
