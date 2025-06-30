from datetime import datetime
from typing import Any

from faker import Faker

from quantiq.modules.assets.domains.assets import AssetType
from tests.faker.scrapper import StockProvider


class AssetFaker(StockProvider):
    def __init__(self, generator: Faker):
        super().__init__(generator)
        self.generator = generator

    def timestamps(self) -> dict[str, datetime]:
        now = self.generator.date_time()
        return {
            "created_at": now,
            "updated_at": now,
        }

    def asset(self) -> dict[str, Any]:
        return {
            **self.timestamps(),
            "ticker": self.ticker(),
            "name": self.name(),
            "type": self.generator.random_element(elements=AssetType),
            "id": self.generator.unique.random_int(min=1, max=1000000),
        }

    def asset_details(self) -> dict[str, Any]:
        asset = self.asset()
        return {
            **self.timestamps(),
            "asset_id": asset["id"],
            "governance": self.generator.random_element(elements=["ON", "PN"]),
            "sector": self.generator.word(),
            "subsector": self.generator.word(),
            "market_value": self.generator.random_int(min=1000000, max=1000000000),
            "last_balance_proccessed": self.generator.date_time(),
            "company_value": self.generator.random_int(min=1000000, max=1000000000),
            "number_of_stocks": self.generator.random_int(min=1000000, max=1000000000),
        }
