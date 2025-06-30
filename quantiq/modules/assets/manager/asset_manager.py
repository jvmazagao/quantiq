from quantiq.modules.assets.domains.assets import Asset
from quantiq.modules.assets.services.asset_service import AssetService
from quantiq.modules.scrapper.providers.fundamentus.data import AssetType
from quantiq.modules.scrapper.strategies.extractor import ExtractorStrategy


class AssetManager:
    def __init__(self, extractor: ExtractorStrategy, asset_service: AssetService):
        self.extractor = extractor
        self.asset_service = asset_service

    def get_asset(self, ticker: str) -> Asset:
        asset = self.asset_service.get_asset_by_ticker(ticker)
        return asset

    def create_asset(self, ticker: str) -> Asset:
        data = self.extractor.execute(AssetType.STOCK, ticker)
        asset = self.asset_service.insert_asset(data)
        if not asset:
            raise ValueError("Asset not found")

        return asset
