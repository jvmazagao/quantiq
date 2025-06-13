from quantiq.modules.financial_results.repositories.financial_results import FinancialResultsRepository
from quantiq.modules.financial_results.services.financial_results import FinancialResultsService

__all__ = ["make_financial_results_service"]

def make_financial_results_repository():
    return FinancialResultsRepository()

def make_financial_results_service():
    return FinancialResultsService(make_financial_results_repository())