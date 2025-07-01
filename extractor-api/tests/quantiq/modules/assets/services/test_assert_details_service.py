from datetime import datetime
from typing import Any
from unittest.mock import Mock, patch

from faker import Faker
from pytest import fixture

from quantiq.modules.assets.domains.assets import AssetDetails
from quantiq.modules.assets.repositories.asset_details_repository import (
    AssetDetailsRepository,
)
from quantiq.modules.assets.services.asset_details_service import AssetDetailsService


class TestAssetDetailsService:
    @fixture
    def asset_details(self, fake: Faker) -> dict[str, Any]:
        return fake.asset_details()

    @fixture
    def ticker(self, fake: Faker) -> str:
        return fake.ticker()

    @fixture
    def service(self, mock_db: Mock) -> AssetDetailsService:
        return AssetDetailsService(AssetDetailsRepository(mock_db))

    def test_get_asset_details_by_ticker(
        self, service: AssetDetailsService, ticker: str, asset_details: dict[str, Any]
    ):
        with patch.object(
            AssetDetailsRepository, "get_by_ticker"
        ) as mock_get_by_ticker:

            def when_get_asset_details_by_ticker():
                mock_get_by_ticker.return_value = None
                response = service.get_asset_details_by_ticker(ticker)
                assert response is None
                mock_get_by_ticker.assert_called_with(ticker)

            def when_get_asset_details_by_ticker_found():
                id = Faker().unique.random_int(min=1, max=1000000)
                asset_details["id"] = id
                mock_get_by_ticker.return_value = AssetDetails(**asset_details)
                response = service.get_asset_details_by_ticker(ticker)
                assert response is not None
                assert response.id == id
                assert response.governance == asset_details["governance"]
                assert response.sector == asset_details["sector"]
                assert response.subsector == asset_details["subsector"]
                assert response.market_value == asset_details["market_value"]
                assert (
                    response.last_balance_proccessed
                    == asset_details["last_balance_proccessed"]
                )
                assert response.company_value == asset_details["company_value"]
                assert response.number_of_stocks == asset_details["number_of_stocks"]
                assert response.asset_id == asset_details["asset_id"]

            when_get_asset_details_by_ticker()
            when_get_asset_details_by_ticker_found()

    def test_insert_asset_details(
        self, service: AssetDetailsService, asset_details: dict[str, Any], ticker: str
    ):
        with patch.object(
            AssetDetailsRepository, "insert"
        ) as mock_insert, patch.object(AssetDetailsRepository, "get_by_ticker"):
            id = Faker().unique.random_int(min=1, max=1000000)
            asset_details["id"] = id
            mock_insert.return_value = AssetDetails(**asset_details)
            response = service.insert_asset_details(
                ticker, AssetDetails(**asset_details)
            )
            assert response is not None
            assert response.id == asset_details["id"]
            assert response.governance == asset_details["governance"]
            assert response.sector == asset_details["sector"]
            assert response.subsector == asset_details["subsector"]
            assert response.market_value == asset_details["market_value"]
            assert (
                response.last_balance_proccessed
                == asset_details["last_balance_proccessed"]
            )
            assert response.company_value == asset_details["company_value"]
            assert response.number_of_stocks == asset_details["number_of_stocks"]
            assert response.asset_id == asset_details["asset_id"]

            mock_insert.assert_called_once_with(AssetDetails(**asset_details))

    def test_not_insert_asset_details_if_is_same_date_as_last_balance_proccessed(
        self, service: AssetDetailsService, asset_details: dict[str, Any], ticker: str
    ):
        with patch.object(
            AssetDetailsRepository, "insert"
        ) as mock_insert, patch.object(
            AssetDetailsRepository, "get_by_ticker"
        ) as mock_get_by_ticker:
            now = datetime.now()
            asset_details["last_balance_proccessed"] = now
            details = AssetDetails(**asset_details)
            mock_get_by_ticker.return_value = details
            response = service.insert_asset_details(ticker, details)
            assert response.id == details.id
            assert response.governance == details.governance
            assert response.sector == details.sector
            assert response.subsector == details.subsector
            assert response.market_value == details.market_value
            assert response.last_balance_proccessed == details.last_balance_proccessed
            assert response.company_value == details.company_value
            assert response.number_of_stocks == details.number_of_stocks
            assert response.asset_id == details.asset_id
            mock_get_by_ticker.assert_called_with(ticker)
            mock_insert.assert_not_called()
