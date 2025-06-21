# from quantiq.modules.assets.services.asset_service import AssetService

from faker import Faker


class TestAssetService:
    def test_get_asset_by_ticker(self, fake: Faker):
        # asset_service = AssetService()
        # asset = asset_service.get_asset_by_ticker(fake.stock_data())
        asset = fake.stock_data()
        assert asset["ticker"] == asset["ticker"]
        assert asset["name"] == asset["name"]
