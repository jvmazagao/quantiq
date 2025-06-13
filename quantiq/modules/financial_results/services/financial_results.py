from quantiq.modules.financial_results.repositories.financial_results import FinancialResultsRepository
from quantiq.modules.financial_results.domains.entities import FinancialResults

class FinancialResultsService:
    def __init__(self, financial_results_repository: FinancialResultsRepository):
        self.financial_results_repository = financial_results_repository

    def store(self, financial_results: dict, stock_id: int):
        financial_results = FinancialResults.parse(financial_results, stock_id)
        stored_financial_results = self.financial_results_repository.store(financial_results)
        return stored_financial_results
    
    def fetch(self, stock_id: int) -> FinancialResults | None:
        return self.financial_results_repository.fetch(stock_id)