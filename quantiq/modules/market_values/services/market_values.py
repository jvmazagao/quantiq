from typing import Any

from quantiq.modules.market_values.domains.entities import MarketValues
from quantiq.modules.market_values.repositories.market_values import (
    MarketValuesRepository,
)


class MarketValuesService:
    def __init__(self, market_values_repository: MarketValuesRepository):
        self.market_values_repository = market_values_repository

    def store(self, data: dict[str, Any], stock_id: int) -> MarketValues:
        market_values = MarketValues.parse(data, stock_id)
        self.market_values_repository.store(market_values)
        return market_values

    def fetch(self, stock_id: int) -> MarketValues | None:
        return self.market_values_repository.fetch(stock_id)
