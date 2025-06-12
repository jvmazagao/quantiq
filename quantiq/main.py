from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from quantiq.modules.stocks.repositories.stock_repository import StockRepository
from quantiq.modules.stocks.use_cases.get_stock import GetStock
from quantiq.modules.stocks.use_cases.insert_stock import InsertStock
from quantiq.modules.scrapper.providers.fundamentus.stock_extractor import FundamentusScraper
from quantiq.modules.scrapper.providers.fundamentus.reit_extractor import FundamentusREITScraper
from quantiq.database.database import create_database
from quantiq.modules.financial_info.repository.financial_info_repository import FinancialInfoRepository
from quantiq.modules.balance_sheet.repositories.balance_sheets_repository import BalanceSheetsRepository
from quantiq.modules.market_values.repositories.market_values_repository import MarketValuesRepository
from quantiq.modules.variations.repositories.variations_repository import VariationsRepository
from quantiq.modules.indicators.repositories.indicator_repository import IndicatorRepository
from quantiq.modules.financial_results.repositories.financial_results_repository import FinancialResultsRepository
from quantiq.modules.stocks.presentation.api.stock_router import StockRouter
from quantiq.modules.balance_sheet.services.service import BalanceSheetService
from quantiq.modules.financial_info.services.service import FinancialInfoService
from quantiq.modules.financial_results.services.services import FinancialResultsService
from quantiq.modules.indicators.services.service import IndicatorService
from quantiq.modules.market_values.services.service import MarketValuesService
from quantiq.modules.variations.services.service import VariationsService
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Quantiq API",
    description="API for scraping stock data from Fundamentus",
    version="1.0.0",
    logger=logger,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stock_scraper = FundamentusScraper()
reit_scraper = FundamentusREITScraper()

insert_stock = InsertStock(
    StockRepository(),
    BalanceSheetService(BalanceSheetsRepository()),
    FinancialInfoService(FinancialInfoRepository()),
    MarketValuesService(MarketValuesRepository()),
    VariationsService(VariationsRepository()),
    IndicatorService(IndicatorRepository()),
    FinancialResultsService(FinancialResultsRepository()),
    stock_scraper
)

get_stock = GetStock(StockRepository())

stock_router = StockRouter(insert_stock, get_stock)

@app.on_event("startup")
async def startup_event():
    create_database()
    logger.info("Database initialized")
    app.include_router(stock_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Quantiq API",
        "endpoints": {
            "/stocks/{ticker}": "Get stock data for a given ticker"
        }
    }

# @app.get("/v1/stocks/{ticker}")
# async def get_stock(ticker: str):
#     try:
#         data = stock_scraper.scrape(ticker)
#         data["basic_info"]["tipo"] = "stock"  # Add type field for regular stocks
        
#         # stored = stock_repository.store(data["basic_info"])
#         details = financial_info_repository.store(data["last_financial_info"], stored["id"])   
#         market_values = market_values_repository.store(data["market_values"], stored["id"])
#         variations = variations_repository.store(data["variations"], stored["id"])
#         indicators = indicator_repository.store(data["indicators"], stored["id"])
#         balance_sheets = balance_sheets_repository.store(data["balance_sheet"], stored["id"])
#         financial_results = financial_results_repository.store(data["financial_results"], stored["id"])

#         return { "data": data }
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))

# @app.get("/reits/{ticker}")
# async def get_reit(ticker: str):
#     try:
#         data = reit_scraper.scrape(ticker)
#         return { "data": data }
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))

# @app.delete("/stocks/{ticker}")
# async def remove_stock(ticker: str):
#     try:
#         stock_repository.delete(ticker)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))

# class StockBatch(BaseModel):
#     tickers: list[str]

# class REITBatch(BaseModel):
#     tickers: list[str]

# @app.post("/stocks/batch")
# async def get_multiple_stocks(body: StockBatch):
#     results = []
#     errors = []
    
#     for ticker in body.tickers:
#         try:
#             data = stock_scraper.scrape(ticker)
#             data["basic_info"]["tipo"] = "stock"  # Add type field for regular stocks
            
#             stored = stock_repository.store(data["basic_info"])
#             details = financial_info_repository.store(data["last_financial_info"], stored["id"])   
#             market_values = market_values_repository.store(data["market_values"], stored["id"])
#             variations = variations_repository.store(data["variations"], stored["id"])
#             indicators = indicator_repository.store(data["indicators"], stored["id"])
#             balance_sheets = balance_sheets_repository.store(data["balance_sheet"], stored["id"])
#             financial_results = financial_results_repository.store(data["financial_results"], stored["id"])

#             results.append({
#                 "ticker": ticker,
#                 "status": "success",
#                 "data": data
#             })
#         except Exception as e:
#             errors.append({
#                 "ticker": ticker,
#                 "status": "error",
#                 "error": str(e)
#             })
    
#     return {
#         "results": results,
#         "errors": errors
#     }

# @app.post("/reits/batch")
# async def get_multiple_reits(body: REITBatch):
#     results = []
#     errors = []
    
#     for ticker in body.tickers:
#         try:
#             data = reit_scraper.scrape(ticker)
#             results.append({
#                 "ticker": ticker,
#                 "status": "success",
#                 "data": data
#             })
#         except Exception as e:
#             errors.append({
#                 "ticker": ticker,
#                 "status": "error",
#                 "error": str(e)
#             })
    
#     return {
#         "results": results,
#         "errors": errors
#     }
