from typing import Any

from quantiq.modules.financial_info.domain.entities import FinancialInfo
from quantiq.modules.financial_info.repository.financial_info_repository import (
    FinancialInfoRepository,
)


class FinancialInfoService:
    def __init__(self, financial_info_repository: FinancialInfoRepository):
        self.financial_info_repository = financial_info_repository

    def store(self, data: dict[str, Any], stock_id: int) -> FinancialInfo:
        financial_info = FinancialInfo.parse(data, stock_id)
        self.financial_info_repository.store(financial_info)
        return financial_info

    def fetch(self, stock_id: int) -> FinancialInfo | None:
        return self.financial_info_repository.fetch(stock_id)
