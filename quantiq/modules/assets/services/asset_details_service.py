from quantiq.modules.assets.domains.assets import AssetDetails
from quantiq.modules.assets.repositories.asset_details_repository import (
    AssetDetailsRepository,
)


class AssetDetailsService:
    def __init__(self, asset_details_repository: AssetDetailsRepository):
        self.asset_details_repository = asset_details_repository

    def get_asset_details_by_ticker(self, ticker: str) -> AssetDetails | None:
        asset_details = self.asset_details_repository.get_by_ticker(ticker)
        return asset_details

    def insert_asset_details(self, ticker: str, data: AssetDetails) -> AssetDetails:
        details = self.get_asset_details_by_ticker(ticker)
        if details and details.last_balance_proccessed == data.last_balance_proccessed:
            return details

        asset_details = self.asset_details_repository.insert(data)
        return asset_details
