from quantiq.modules.balance_sheet.dependencies import make_balance_sheet_service
from quantiq.modules.financial_info.dependencies import make_financial_info_service
from quantiq.modules.financial_results.dependencies import (
    make_financial_results_service,
)
from quantiq.modules.indicators.dependencies import make_indicators_service
from quantiq.modules.market_values.dependencies import make_market_values_service
from quantiq.modules.scrapper.dependencies import make_extractor_strategy
from quantiq.modules.stocks.presentation.api.stock_router import StockRouter
from quantiq.modules.stocks.repositories.stock_repository import StockRepository
from quantiq.modules.stocks.services.stock_services import StockServices
from quantiq.modules.stocks.use_cases.get_stock import GetStock
from quantiq.modules.stocks.use_cases.insert_stock import InsertStock
from quantiq.modules.variations.dependencies import make_variations_service

__all__ = ["make_stock_services"]


def make_stock_repository() -> StockRepository:
    return StockRepository()


def make_stock_services() -> StockServices:
    return StockServices(
        make_stock_repository(),
        make_balance_sheet_service(),
        make_financial_info_service(),
        make_market_values_service(),
        make_variations_service(),
        make_indicators_service(),
        make_financial_results_service(),
    )


def make_insert_stock() -> InsertStock:
    return InsertStock(
        make_stock_repository(),
        make_balance_sheet_service(),
        make_financial_info_service(),
        make_market_values_service(),
        make_variations_service(),
        make_indicators_service(),
        make_financial_results_service(),
        make_extractor_strategy(),
    )


def make_get_stock() -> GetStock:
    return GetStock(make_stock_services())


def make_stock_router() -> StockRouter:
    return StockRouter(make_insert_stock(), make_get_stock())
