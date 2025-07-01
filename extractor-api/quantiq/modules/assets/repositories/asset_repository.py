from datetime import datetime

from quantiq.core.infra.databases.sqlite.sqlite import Sqlite
from quantiq.core.logging.base_logger import get_logger
from quantiq.modules.assets.domains.assets import Asset
from quantiq.modules.scrapper.providers.fundamentus.data import AssetType


class AssetRepository:
    def __init__(self, db: Sqlite):
        self.logger = get_logger(__name__)
        self.db = db

    def get_by_ticker(self, ticker: str) -> Asset | None:
        query = "SELECT id, ticker, name, type, created_at, updated_at FROM assets WHERE ticker = :ticker"
        params = {"ticker": ticker}
        data = self.db.fetch_one(query, params)
        if data:
            (id, _, name, type, created_at, updated_at) = data
            return Asset(
                id=int(id),
                ticker=ticker,
                name=name,
                type=AssetType(type),
                created_at=datetime.fromisoformat(created_at),
                updated_at=datetime.fromisoformat(updated_at),
            )
        return None

    def insert(self, data: Asset) -> Asset | None:
        try:
            query = """
                INSERT INTO assets (ticker, name, type) VALUES (?, ?, ?)
                ON CONFLICT(ticker) DO UPDATE SET
                    name = excluded.name,
                    type = excluded.type,
                    updated_at = datetime('now', 'utc')
                RETURNING id, ticker, name, type, created_at, updated_at
            """
            result = self.db.upsert(query, (data.ticker, data.name, data.type.value))
            data.id = result
            return data
        except Exception as e:
            self.logger.error(f"Error inserting asset: {e}")
            raise e
