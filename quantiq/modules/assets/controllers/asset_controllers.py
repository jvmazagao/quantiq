from fastapi import APIRouter, Response

from quantiq.modules.assets.manager.asset_manager import AssetManager


class AssetController(APIRouter):
    def __init__(self, service: AssetManager):
        super().__init__(prefix="/assets", tags=["assets"])
        self.service = service
        self.register_routes()

    def insert_asset(self, ticker: str) -> Response:
        asset = self.service.create_asset(ticker)
        return Response(
            status_code=201,
            content=asset.model_dump_json(),
            media_type="application/json",
        )

    def register_routes(self) -> None:
        self.add_api_route("/{ticker}", self.insert_asset, methods=["POST"])
