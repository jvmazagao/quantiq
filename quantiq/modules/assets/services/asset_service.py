from typing import Any

from quantiq.core.errors import NotFoundException
from quantiq.modules.assets.domains.assets import Asset, AssetDetails
from quantiq.modules.assets.repositories.asset_repository import AssetRepository
from quantiq.modules.assets.services.asset_details_service import AssetDetailsService


class AssetNotFoundError(NotFoundException):
    def __init__(self, ticker: str):
        super().__init__(detail={"ticker": ticker})


class AssetService:
    def __init__(
        self,
        asset_repository: AssetRepository,
        asset_details_service: AssetDetailsService,
    ):
        self.asset_repository = asset_repository
        self.asset_details_service = asset_details_service

    def get_asset_by_ticker(self, ticker: str) -> Asset:
        asset = self.asset_repository.get_by_ticker(ticker)
        if asset is None:
            raise AssetNotFoundError(ticker)
        return asset

    def insert_asset(self, data: dict[str, Any]) -> Asset:
        asset = self.asset_repository.get_by_ticker(data["ticker"])

        if not asset:
            asset = self.asset_repository.insert(
                Asset(
                    ticker=data["ticker"],
                    type=data["type"],
                    name=data["name"],
                )
            )

        if not asset:
            raise ValueError("Asset not found")

        asset_details = AssetDetails(
            asset_id=asset.id,
            governance=data["governance"],
            sector=data["sector"],
            subsector=data["subsector"],
            market_value=data["market_value"],
            last_balance_proccessed=data["last_balance_proccessed"],
            company_value=data["company_value"],
            number_of_stocks=data["number_of_stocks"],
        )
        details = self.asset_details_service.insert_asset_details(
            data["ticker"], asset_details
        )
        asset.asset_details = details

        return asset
