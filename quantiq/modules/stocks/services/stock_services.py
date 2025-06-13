from quantiq.modules.stocks.repositories.stock_repository import StockRepository
from quantiq.modules.stocks.errors import StockNotFoundException
from quantiq.modules.balance_sheet.services.service import BalanceSheetService
from quantiq.modules.financial_info.services.service import FinancialInfoService
from quantiq.modules.market_values.services.market_values import MarketValuesService
from quantiq.modules.variations.services.variations import VariationsService
from quantiq.modules.indicators.services.indicators import IndicatorService
from quantiq.modules.financial_results.services.financial_results import FinancialResultsService

class StockServices:
    def __init__(self, stock_repository: StockRepository, balance_sheet_service: BalanceSheetService, financial_info_service: FinancialInfoService, market_values_service: MarketValuesService, variations_service: VariationsService, indicators_service: IndicatorService, financial_results_service: FinancialResultsService):
        self.stock_repository = stock_repository
        self.balance_sheet_service = balance_sheet_service
        self.financial_info_service = financial_info_service
        self.market_values_service = market_values_service
        self.variations_service = variations_service
        self.indicators_service = indicators_service
        self.financial_results_service = financial_results_service
        
    def get_stock(self, ticker: str):
        stock = self.stock_repository.fetch(ticker)
        if not stock:
            raise StockNotFoundException(ticker)
        
        balance_sheet = self.balance_sheet_service.fetch(stock.id)
        financial_info = self.financial_info_service.fetch(stock.id)
        market_values = self.market_values_service.fetch(stock.id)
        variations = self.variations_service.fetch(stock.id)
        indicators = self.indicators_service.fetch(stock.id)
        financial_results = self.financial_results_service.fetch(stock.id)
        
        return {
            "stock": stock,
            "balance_sheet": balance_sheet,
            "financial_info": financial_info,
            "market_values": market_values,
            "variations": variations,
            "indicators": indicators,
            "financial_results": financial_results
        }