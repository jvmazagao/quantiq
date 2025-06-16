from quantiq.modules.market_values.repositories.market_values import (
    MarketValuesRepository,
)
from quantiq.modules.market_values.services.market_values import MarketValuesService

__all__ = ["make_market_values_service"]


def make_market_values_repository() -> MarketValuesRepository:
    return MarketValuesRepository()


def make_market_values_service() -> MarketValuesService:
    return MarketValuesService(make_market_values_repository())
