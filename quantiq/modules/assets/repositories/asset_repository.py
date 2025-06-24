from quantiq.core.infra.databases.sqlite.sqlite import Sqlite
from quantiq.core.logging.base_logger import get_logger
from quantiq.modules.assets.domains.assets import Asset
from quantiq.modules.assets.errors import AssetNotInsertedError


class AssetRepository:
    def __init__(self, db: Sqlite):
        self.logger = get_logger(__name__)
        self.db = db

    def get_by_ticker(self, ticker: str) -> Asset | None:
        data = self.db.fetch_one("SELECT * FROM stocks WHERE ticker = ?", (ticker,))
        if data:
            return Asset.create(data)
        return None

    def insert(self, data: Asset) -> Asset:
        try:
            query = """
                INSERT INTO stocks (ticker, name, type) VALUES (?, ?, ?)
                ON CONFLICT(ticker) DO UPDATE SET
                    name = excluded.name,
                    type = excluded.type,
                    updated_at = NOW()
                RETURNING id, name, type, created_at, updated_at
            """
            result = self.db.upsert(query, (data.ticker, data.name, data.type.value))
            if not result or isinstance(result, int):
                raise AssetNotInsertedError()
            return Asset.create(result)
        except Exception as e:
            self.logger.error(f"Error inserting asset: {e}")
            raise e
