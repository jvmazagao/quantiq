from quantiq.modules.stocks.domain.entities import Stock
from quantiq.modules.stocks.repositories.stock_repository import StockRepository

from quantiq.modules.balance_sheet.services.service import BalanceSheetService
from quantiq.modules.financial_info.services.service import FinancialInfoService
from quantiq.modules.market_values.services.market_values import MarketValuesService
from quantiq.modules.variations.repositories.variations import VariationsRepository
from quantiq.modules.financial_results.services.financial_results import FinancialResultsService
from quantiq.modules.indicators.services.indicators import IndicatorService
from quantiq.modules.variations.services.variations import VariationsService
from quantiq.modules.scrapper.dependencies import make_extractor_strategy
from quantiq.modules.scrapper.strategies.extractor import ExtractorStrategy

class InsertStock:
    def __init__(
            self,
            stock_repository: StockRepository,
            balance_sheet_service: BalanceSheetService,
            financial_info_service: FinancialInfoService,
            market_values_service: MarketValuesService,
            variations_service: VariationsService,
            indicators_service: IndicatorService,
            financial_results_service: FinancialResultsService,
            extractor_strategy: ExtractorStrategy
        ):
        self.stock_repository = stock_repository
        self.extractor_strategy = extractor_strategy
        self.balance_sheet_service = balance_sheet_service
        self.financial_info_service = financial_info_service
        self.market_values_service = market_values_service
        self.variations_service = variations_service
        self.indicators_service = indicators_service
        self.financial_results_service = financial_results_service
        
    def execute(self, type:str, ticker: str):
        stock_data = self.extractor_strategy.execute(type, ticker)
        
        if not stock_data:
            raise ValueError(f"Stock data not found for ticker: {ticker}")
        
        stock_data["basic_info"]["tipo"] = type
        stock = self.stock_repository.store(Stock.parse(stock_data["basic_info"]))
        balance_sheets = self.balance_sheet_service.store(stock_data["balance_sheet"], stock.id)
        financial_info = self.financial_info_service.store(stock_data["last_financial_info"], stock.id)
        market_values = self.market_values_service.store(stock_data["market_values"], stock.id)
        variations = self.variations_service.store(stock_data["variations"], stock.id)
        indicators = self.indicators_service.store(stock_data["indicators"], stock.id)
        financial_results = self.financial_results_service.store(stock_data["financial_results"], stock.id)

        return {
            "stock": stock,
            "balance_sheets": balance_sheets,
            "financial_info": financial_info
        }