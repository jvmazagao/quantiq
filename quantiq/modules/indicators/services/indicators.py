from quantiq.modules.indicators.repositories.indicators import IndicatorRepository
from quantiq.modules.indicators.domains.entities import Indicator

class IndicatorService:
    def __init__(self, indicator_repository: IndicatorRepository):
        self.indicator_repository = indicator_repository

    def store(self, indicators: dict, stock_id: int):
        indicators = Indicator.parse(indicators, stock_id)
        stored_indicators = self.indicator_repository.store(indicators)
        return stored_indicators
    
    def fetch(self, stock_id: int) -> Indicator | None:
        return self.indicator_repository.fetch(stock_id)