from datetime import datetime

from quantiq.core.infra.databases.sqlite.sqlite import Sqlite
from quantiq.modules.assets.domains.assets import AssetDetails


class AssetDetailsRepository:
    def __init__(self, db: Sqlite):
        self.db = db

    def get_by_ticker(self, ticker: str) -> AssetDetails | None:
        query = """
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
        params = {"ticker": ticker}
        data = self.db.fetch_one(query, params)
        if data:
            (
                id,
                governance,
                sector,
                subsector,
                market_value,
                last_balance_proccessed,
                company_value,
                number_of_stocks,
                asset_id,
                created_at,
                updated_at,
            ) = data
            return AssetDetails(
                id=int(id),
                governance=governance,
                sector=sector,
                subsector=subsector,
                market_value=market_value,
                last_balance_proccessed=last_balance_proccessed,
                company_value=company_value,
                number_of_stocks=number_of_stocks,
                created_at=datetime.fromisoformat(created_at),
                updated_at=datetime.fromisoformat(updated_at),
                asset_id=int(asset_id),
            )

        return None

    def insert(self, data: AssetDetails) -> AssetDetails:
        query = """
            INSERT INTO asset_details (asset_id, governance, sector, subsector, market_value, last_balance_proccessed, company_value, number_of_stocks)
            VALUES (:asset_id, :governance, :sector, :subsector, :market_value, :last_balance_proccessed, :company_value, :number_of_stocks)
        """
        params = {
            "asset_id": data.asset_id,
            "governance": data.governance,
            "sector": data.sector,
            "subsector": data.subsector,
            "market_value": data.market_value,
            "last_balance_proccessed": data.last_balance_proccessed,
            "company_value": data.company_value,
            "number_of_stocks": data.number_of_stocks,
        }
        id = self.db.upsert(query, params)
        data.id = int(id)
        return data
