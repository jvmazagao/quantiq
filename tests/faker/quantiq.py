from typing import Any

from faker import Faker

from quantiq.modules.assets.domains.assets import AssetType
from tests.faker.scrapper import StockProvider


class AssetFaker(StockProvider):
    def __init__(self, generator: Faker):
        super().__init__(generator)
        self.generator = generator

    def asset(self) -> dict[str, Any]:
        return {
            "ticker": self.ticker(),
            "name": self.name(),
            "type": self.generator.random_element(elements=AssetType),
            "id": self.generator.unique.random_int(min=1, max=1000000),
            "created_at": self.generator.date_time(),
            "updated_at": self.generator.date_time(),
        }
