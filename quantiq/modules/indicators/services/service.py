from quantiq.modules.indicators.repositories.indicator_repository import IndicatorRepository
from quantiq.modules.indicators.domains.entities import Indicator

class IndicatorService:
    def __init__(self, indicator_repository: IndicatorRepository):
        self.indicator_repository = indicator_repository

    def store(self, indicators: dict, stock_id: int):
        indicators = Indicator.parse(indicators, stock_id)
        stored_indicators = self.indicator_repository.store(indicators)
        return stored_indicators