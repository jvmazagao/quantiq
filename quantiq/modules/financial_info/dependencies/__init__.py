from quantiq.modules.financial_info.repository.financial_info_repository import FinancialInfoRepository
from quantiq.modules.financial_info.services.service import FinancialInfoService

__all__ = ["make_financial_info_service"]

def make_financial_info_repository():
    return FinancialInfoRepository()

def make_financial_info_service():
    return FinancialInfoService(make_financial_info_repository())