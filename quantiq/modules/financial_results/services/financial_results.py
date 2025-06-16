from typing import Any

from quantiq.modules.financial_results.domains.entities import FinancialResults
from quantiq.modules.financial_results.repositories.financial_results import (
    FinancialResultsRepository,
)


class FinancialResultsService:
    def __init__(self, financial_results_repository: FinancialResultsRepository):
        self.financial_results_repository = financial_results_repository

    def store(self, data: dict[str, Any], stock_id: int) -> FinancialResults:
        financial_results = FinancialResults.parse(data, stock_id)
        self.financial_results_repository.store(financial_results)
        return financial_results

    def fetch(self, stock_id: int) -> FinancialResults | None:
        return self.financial_results_repository.fetch(stock_id)
