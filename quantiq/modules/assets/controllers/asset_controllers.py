from fastapi import APIRouter

from quantiq.modules.assets.domains.assets import Asset
from quantiq.modules.assets.manager.asset_manager import AssetManager


class AssetController(APIRouter):
    def __init__(self, service: AssetManager):
        super().__init__(prefix="/assets", tags=["assets"])
        self.service = service
        self.register_routes()

    def insert_asset(self, ticker: str) -> Asset:
        asset = self.service.create_asset(ticker)
        return asset

    def register_routes(self) -> None:
        self.add_api_route("/{ticker}", self.insert_asset, methods=["POST"])
