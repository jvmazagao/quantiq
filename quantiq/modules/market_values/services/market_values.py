from quantiq.modules.market_values.repositories.market_values import MarketValuesRepository
from quantiq.modules.market_values.domains.entities import MarketValues

class MarketValuesService:
    def __init__(self, market_values_repository: MarketValuesRepository):
        self.market_values_repository = market_values_repository

    def store(self, market_values: dict, stock_id: int):
        market_values = MarketValues.parse(market_values, stock_id)
        stored_market_values = self.market_values_repository.store(market_values)
        return stored_market_values

    def fetch(self, stock_id: int) -> MarketValues | None:
        return self.market_values_repository.fetch(stock_id)