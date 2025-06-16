from quantiq.modules.financial_info.repository.financial_info_repository import (
    FinancialInfoRepository,
)
from quantiq.modules.financial_info.services.service import FinancialInfoService

__all__ = ["make_financial_info_service"]


def make_financial_info_repository() -> FinancialInfoRepository:
    return FinancialInfoRepository()


def make_financial_info_service() -> FinancialInfoService:
    return FinancialInfoService(make_financial_info_repository())
