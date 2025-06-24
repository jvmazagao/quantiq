from typing import Any

from quantiq.core.errors import NotFoundException
from quantiq.modules.assets.domains.assets import Asset


class AssetRepository:
    def get_by_ticker(self, ticker: str) -> Asset | None:
        pass

    def insert(self, asset: Asset) -> Asset:
        pass


class AssetNotFoundError(NotFoundException):
    def __init__(self, ticker: str):
        super().__init__(detail={"ticker": ticker})


class AssetService:
    def __init__(self, asset_repository: AssetRepository):
        self.asset_repository = asset_repository

    def get_asset_by_ticker(self, ticker: str) -> Asset:
        asset = self.asset_repository.get_by_ticker(ticker)
        if asset is None:
            raise AssetNotFoundError(ticker)
        return asset

    def insert_asset(self, data: dict[str, Any]) -> Asset:
        asset = self.asset_repository.get_by_ticker(data["ticker"])

        if asset:
            return asset

        return self.asset_repository.insert(Asset.create(data))
