from quantiq.modules.indicators.repositories.indicators import IndicatorRepository
from quantiq.modules.indicators.services.indicators import IndicatorService

__all__ = ["make_indicators_service"]


def make_indicators_repository() -> IndicatorRepository:
    return IndicatorRepository()


def make_indicators_service() -> IndicatorService:
    return IndicatorService(make_indicators_repository())
