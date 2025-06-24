from typing import Any
from unittest.mock import Mock

from faker import Faker
from pytest import fixture, mark, raises

from quantiq.modules.assets.domains.assets import Asset
from quantiq.modules.assets.errors import AssetNotInsertedError
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
        mock_db.fetch_one.assert_called_once_with(
            "SELECT * FROM stocks WHERE ticker = ?", (ticker,)
        )

    def test_get_by_ticker_found(
        self, asset: dict[str, Any], repository: AssetRepository, mock_db: Mock
    ):
        mock_db.fetch_one.return_value = asset

        response = repository.get_by_ticker(asset["ticker"])
        assert response is not None
        assert response.ticker == asset["ticker"]
        assert response.name == asset["name"]
        assert response.type.value == asset["type"]

    def test_insert_asset(
        self, asset: dict[str, Any], repository: AssetRepository, mock_db: Mock
    ):
        data = Asset.create(asset)
        identifier = 1
        mock_db.upsert.return_value = {**asset, "id": identifier}
        response = repository.insert(data)
        assert response is not None
        assert response.ticker == asset["ticker"]
        assert response.name == asset["name"]
        assert response.type.value == asset["type"]
        assert response.id == identifier

        query = """
                INSERT INTO stocks (ticker, name, type) VALUES (?, ?, ?)
                ON CONFLICT(ticker) DO UPDATE SET
                    name = excluded.name,
                    type = excluded.type,
                    updated_at = NOW()
                RETURNING id, name, type, created_at, updated_at
            """

        mock_db.upsert.assert_called_once_with(
            query, (asset["ticker"], asset["name"], asset["type"])
        )

    @mark.parametrize("result", [None, Faker().pyint()])
    def test_insert_asset_return_exception(
        self,
        asset: dict[str, Any],
        repository: AssetRepository,
        mock_db: Mock,
        result: int | None,
    ):
        data = Asset.create(asset)
        mock_db.upsert.return_value = result
        with raises(AssetNotInsertedError) as e:
            repository.insert(data)
        assert e.value.detail == {"message": "Asset not inserted"}
