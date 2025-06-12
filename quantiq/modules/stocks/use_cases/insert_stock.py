from quantiq.modules.stocks.domain.entities import Stock
from quantiq.modules.stocks.repositories.stock_repository import StockRepository

from quantiq.modules.balance_sheet.services.service import BalanceSheetService
from quantiq.modules.financial_info.services.service import FinancialInfoService
from quantiq.modules.market_values.services.service import MarketValuesService
from quantiq.modules.variations.repositories.variations_repository import VariationsRepository
from quantiq.modules.financial_results.services.services import FinancialResultsService
from quantiq.modules.indicators.services.service import IndicatorService
from quantiq.modules.variations.services.service import VariationsService
from quantiq.modules.scrapper.providers.fundamentus.stock_extractor import FundamentusScraper

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
            stock_scraper: FundamentusScraper
        ):
        self.stock_repository = stock_repository
        self.stock_scraper = stock_scraper
        self.balance_sheet_service = balance_sheet_service
        self.financial_info_service = financial_info_service
        self.market_values_service = market_values_service
        self.variations_service = variations_service
        self.indicators_service = indicators_service
        self.financial_results_service = financial_results_service
        
    def execute(self, ticker: str):
        stock_data = self.stock_scraper.scrape(ticker)
        
        if not stock_data:
            raise ValueError(f"Stock data not found for ticker: {ticker}")
        
        stock_data["basic_info"]["tipo"] = "stock"
        stock = self.stock_repository.store(Stock.parse(stock_data["basic_info"]))
        balance_sheets = self.balance_sheet_service.store(stock_data["balance_sheet"], stock["id"])
        financial_info = self.financial_info_service.store(stock_data["last_financial_info"], stock["id"])
        market_values = self.market_values_service.store(stock_data["market_values"], stock["id"])
        variations = self.variations_service.store(stock_data["variations"], stock["id"])
        indicators = self.indicators_service.store(stock_data["indicators"], stock["id"])
        financial_results = self.financial_results_service.store(stock_data["financial_results"], stock["id"])

        return {
            "stock": stock,
            "balance_sheets": balance_sheets,
            "financial_info": financial_info
        }