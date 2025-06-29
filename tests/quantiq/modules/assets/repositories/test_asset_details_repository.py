from typing import Any
from unittest.mock import Mock

from faker import Faker
from pytest import fixture

from quantiq.modules.assets.domains.assets import AssetDetails
from quantiq.modules.assets.repositories.asset_details_repository import (
    AssetDetailsRepository,
)


class TestAssetDetailsRepository:
    select_query = """
            SELECT
                ad.id,
                ad.governance,
                ad.sector,
                ad.subsector,
                ad.market_value,
                ad.last_balance_proccessed,
                ad.company_value,
                ad.number_of_stocks,
                ad.asset_id,
                ad.created_at,
                ad.updated_at
            FROM asset_details ad
            INNER JOIN assets a ON ad.asset_id = a.id
            WHERE a.ticker = :ticker
            ORDER BY ad.created_at DESC
            LIMIT 1
        """

    @fixture
    def asset_details(self, fake: Faker) -> dict[str, Any]:
        return fake.asset_details()

    @fixture
    def ticker(self, fake: Faker) -> str:
        return fake.ticker()

    @fixture
    def repository(self, mock_db: Mock) -> AssetDetailsRepository:
        return AssetDetailsRepository(mock_db)

    def test_get_by_ticker_and_return_none(
        self, fake: Faker, repository: AssetDetailsRepository, mock_db: Mock
    ):
        ticker = fake.ticker()
        mock_db.fetch_one.return_value = None
        asset_details = repository.get_by_ticker(ticker)
        assert asset_details is None
        params = {"ticker": ticker}
        mock_db.fetch_one.assert_called_once_with(self.select_query, params)

    def test_get_by_ticker_found(
        self,
        asset_details: dict[str, Any],
        ticker: str,
        repository: AssetDetailsRepository,
        mock_db: Mock,
    ):
        asset_details["id"] = Faker().unique.random_int(min=1, max=1000000)
        asset_details["ticker"] = ticker
        mock_db.fetch_one.return_value = (
            asset_details["id"],
            asset_details["governance"],
            asset_details["sector"],
            asset_details["subsector"],
            asset_details["market_value"],
            asset_details["last_balance_proccessed"],
            asset_details["company_value"],
            asset_details["number_of_stocks"],
            asset_details["asset_id"],
            asset_details["created_at"].isoformat(),
            asset_details["updated_at"].isoformat(),
        )
        response = repository.get_by_ticker(ticker)
        assert response is not None
        assert response.id == asset_details["id"]
        assert response.governance == asset_details["governance"]
        assert response.sector == asset_details["sector"]
        assert response.subsector == asset_details["subsector"]
        assert response.market_value == asset_details["market_value"]
        assert (
            response.last_balance_proccessed == asset_details["last_balance_proccessed"]
        )
        assert response.company_value == asset_details["company_value"]
        assert response.number_of_stocks == asset_details["number_of_stocks"]
        assert response.asset_id == asset_details["asset_id"]
        assert response.created_at == asset_details["created_at"]
        assert response.updated_at == asset_details["updated_at"]

    def test_insert_asset_details(
        self,
        asset_details: dict[str, Any],
        ticker: str,
        repository: AssetDetailsRepository,
        mock_db: Mock,
    ):
        asset_details["ticker"] = ticker
        mock_db.upsert.return_value = 1
        data = AssetDetails(
            governance=asset_details["governance"],
            sector=asset_details["sector"],
            subsector=asset_details["subsector"],
            market_value=asset_details["market_value"],
            last_balance_proccessed=asset_details["last_balance_proccessed"],
            company_value=asset_details["company_value"],
            number_of_stocks=asset_details["number_of_stocks"],
            asset_id=asset_details["asset_id"],
        )
        response = repository.insert(data)
        assert response.id == 1
