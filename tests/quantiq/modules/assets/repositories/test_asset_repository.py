from datetime import datetime
from typing import Any
from unittest.mock import Mock

from faker import Faker
from pytest import fixture

from quantiq.modules.assets.domains.assets import Asset
from quantiq.modules.assets.repositories.asset_repository import AssetRepository


class TestAssetRepository:
    @fixture
    def asset(self, fake: Faker) -> dict[str, Any]:
        return fake.stock_data()

    @fixture
    def repository(self, mock_db: Mock) -> AssetRepository:
        return AssetRepository(mock_db)

    def test_get_by_ticker_and_return_none(
        self, fake: Faker, repository: AssetRepository, mock_db: Mock
    ):
        ticker = fake.ticker()
        asset = repository.get_by_ticker(ticker)
        assert asset is None
        query = "SELECT id, ticker, name, type, created_at, updated_at FROM assets WHERE ticker = :ticker"
        params = {"ticker": ticker}
        mock_db.fetch_one.assert_called_once_with(query, params)

    def test_get_by_ticker_found(
        self, asset: dict[str, Any], repository: AssetRepository, mock_db: Mock
    ):
        now = datetime.now().isoformat()
        created_at, updated_at = now, now
        id = 1
        mock_db.fetch_one.return_value = (
            id,
            asset["ticker"],
            asset["name"],
            asset["type"].value,
            created_at,
            updated_at,
        )

        response = repository.get_by_ticker(asset["ticker"])
        assert response is not None
        assert response.ticker == asset["ticker"]
        assert response.name == asset["name"]
        assert response.type == asset["type"]
        assert response.created_at == datetime.fromisoformat(created_at)
        assert response.updated_at == datetime.fromisoformat(updated_at)

    def test_insert_asset(
        self, asset: dict[str, Any], repository: AssetRepository, mock_db: Mock
    ):
        data = Asset.create(asset)
        identifier = 1
        mock_db.upsert.return_value = identifier
        response = repository.insert(data)
        assert response is not None
        assert response.ticker == asset["ticker"]
        assert response.name == asset["name"]
        assert response.type == asset["type"]
        assert response.id == identifier

        query = """
                INSERT INTO assets (ticker, name, type) VALUES (?, ?, ?)
                ON CONFLICT(ticker) DO UPDATE SET
                    name = excluded.name,
                    type = excluded.type,
                    updated_at = datetime('now', 'utc')
                RETURNING id, ticker, name, type, created_at, updated_at
            """

        mock_db.upsert.assert_called_once_with(
            query, (asset["ticker"], asset["name"], asset["type"].value)
        )
