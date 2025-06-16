from typing import Any

from quantiq.modules.indicators.domains.entities import Indicator
from quantiq.modules.indicators.repositories.indicators import IndicatorRepository


class IndicatorService:
    def __init__(self, indicator_repository: IndicatorRepository):
        self.indicator_repository = indicator_repository

    def store(self, data: dict[str, Any], stock_id: int) -> Indicator:
        indicators = Indicator.parse(data, stock_id)
        self.indicator_repository.store(indicators)
        return indicators

    def fetch(self, stock_id: int) -> Indicator | None:
        return self.indicator_repository.fetch(stock_id)
