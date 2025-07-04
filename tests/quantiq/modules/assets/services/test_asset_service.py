from datetime import datetime
from typing import Any
from unittest.mock import Mock, patch

from faker import Faker
from pytest import fixture, raises

from quantiq.modules.assets.domains.assets import Asset, AssetType
from quantiq.modules.assets.repositories.asset_repository import AssetRepository
from quantiq.modules.assets.services.asset_details_service import AssetDetailsService
from quantiq.modules.assets.services.asset_service import (
    AssetNotFoundError,
    AssetService,
)


class TestAssetService:
    @fixture
    def asset(self, fake: Faker) -> dict[str, Any]:
        return fake.stock_data()

    @fixture
    def asset_details(self, fake: Faker) -> dict[str, Any]:
        return fake.asset_details()

    @fixture
    def service(self, mock_db: Mock) -> AssetService:
        return AssetService(AssetRepository(mock_db), AssetDetailsService(mock_db))

    def test_get_asset_by_ticker(self, asset: dict[str, Any], service: AssetService):
        with patch.object(AssetRepository, "get_by_ticker") as mock_get_by_ticker:

            def when_get_asset_by_ticker():
                mock_get_by_ticker.return_value = Asset.create(asset)
                model = service.get_asset_by_ticker(asset["ticker"])
                mock_get_by_ticker.assert_called_once_with(asset["ticker"])
                assert model.ticker == asset["ticker"]
                assert model.name == asset["name"]
                assert model.type == AssetType.STOCK

            def when_get_asset_by_ticker_not_found():
                mock_get_by_ticker.return_value = None
                with raises(AssetNotFoundError) as e:
                    service.get_asset_by_ticker(asset["ticker"])
                assert e.value.detail == {"ticker": asset["ticker"]}
                assert e.value.status_code == 404

            when_get_asset_by_ticker()
            when_get_asset_by_ticker_not_found()

    def test_insert_asset(
        self,
        asset: dict[str, Any],
        asset_details: dict[str, Any],
        service: AssetService,
    ):
        with patch.object(AssetRepository, "get_by_ticker") as mock_get_by_ticker:  # noqa: SIM117
            with patch.object(AssetRepository, "insert") as mock_insert, patch.object(
                AssetDetailsService, "insert_asset_details"
            ):

                def when_insert_asset():
                    data = {
                        **asset,
                        **asset_details,
                    }
                    asset_data = Asset.create({**asset})
                    expected_asset = Asset.create(data)
                    mock_get_by_ticker.return_value = None
                    mock_insert.return_value = expected_asset
                    created_asset = service.insert_asset(data)

                    mock_get_by_ticker.assert_called_with(asset["ticker"])
                    mock_insert.assert_called_once_with(asset_data)

                    assert created_asset.ticker == expected_asset.ticker
                    assert created_asset.name == expected_asset.name
                    assert created_asset.type == expected_asset.type
                    assert created_asset.id == expected_asset.id
                    assert created_asset.created_at == expected_asset.created_at
                    assert created_asset.updated_at == expected_asset.updated_at

                def when_insert_asset_already_exists():
                    date = datetime.now()
                    expected_asset = Asset.create(
                        {**asset, "id": 1, "created_at": date, "updated_at": date}
                    )
                    mock_get_by_ticker.return_value = expected_asset
                    created_asset = service.insert_asset(asset)

                    mock_get_by_ticker.assert_called_with(asset["ticker"])

                    assert created_asset.ticker == expected_asset.ticker
                    assert created_asset.name == expected_asset.name
                    assert created_asset.type == expected_asset.type
                    assert created_asset.id == expected_asset.id
                    assert created_asset.created_at == expected_asset.created_at
                    assert created_asset.updated_at == expected_asset.updated_at

                when_insert_asset()
                when_insert_asset_already_exists()
