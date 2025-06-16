from quantiq.modules.financial_results.repositories.financial_results import (
    FinancialResultsRepository,
)
from quantiq.modules.financial_results.services.financial_results import (
    FinancialResultsService,
)

__all__ = ["make_financial_results_service"]


def make_financial_results_repository() -> FinancialResultsRepository:
    return FinancialResultsRepository()


def make_financial_results_service() -> FinancialResultsService:
    return FinancialResultsService(make_financial_results_repository())
