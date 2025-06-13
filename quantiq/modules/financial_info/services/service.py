from quantiq.modules.financial_info.repository.financial_info_repository import FinancialInfoRepository
from quantiq.modules.financial_info.domain.entities import FinancialInfo

class FinancialInfoService:
    def __init__(self, financial_info_repository: FinancialInfoRepository):
        self.financial_info_repository = financial_info_repository

    def store(self, financial_info: dict, stock_id: int):
        financial_info = FinancialInfo.parse(financial_info, stock_id)
        self.financial_info_repository.store(financial_info)
        return financial_info.id
    
    def fetch(self, stock_id: int) -> FinancialInfo | None:
        return self.financial_info_repository.fetch(stock_id)