from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from quantiq.scraper import FundamentusScraper
from quantiq.database.database import transaction, create_database
from quantiq.repositories.stock_repository import StockRepository
from quantiq.repositories.financial_info_repository import FinancialInfoRepository
from quantiq.repositories.market_values_repository import MarketValuesRepository
from quantiq.repositories.variations_repository import VariationsRepository
from quantiq.repositories.indicator_repository import IndicatorRepository
from quantiq.repositories.balance_sheets_repository import BalanceSheetsRepository
from quantiq.repositories.financial_results_repository import FinancialResultsRepository

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

# Initialize scraper
scraper = FundamentusScraper()
stock_repository = StockRepository()
financial_info_repository = FinancialInfoRepository()
market_values_repository = MarketValuesRepository()
variations_repository = VariationsRepository()
indicator_repository = IndicatorRepository()
balance_sheets_repository = BalanceSheetsRepository()
financial_results_repository = FinancialResultsRepository()

@app.on_event("startup")
async def startup_event():
    create_database()
    logger.info("Database initialized")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Quantiq API",
        "endpoints": {
            "/stocks/{ticker}": "Get stock data for a given ticker"
        }
    }

@app.get("/stocks/{ticker}")
async def get_stock(ticker: str):
    try:
        data = scraper.scrape(ticker)
        stored = stock_repository.store(data["basic_info"])
        details = financial_info_repository.store(data["last_financial_info"], stored["id"])   
        market_values = market_values_repository.store(data["market_values"], stored["id"])
        variations = variations_repository.store(data["variations"], stored["id"])
        indicators = indicator_repository.store(data["indicators"], stored["id"])
        balance_sheets = balance_sheets_repository.store(data["balance_sheet"], stored["id"])
        financial_results = financial_results_repository.store(data["financial_results"], stored["id"])

        return { "data": data }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 
    
@app.delete("/stocks/{ticker}")
async def remove_stock(ticker: str):
    try:
        stock_repository.delete(ticker)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

class StockBatch(BaseModel):
    tickers: list[str]

@app.post("/stocks/batch")
async def get_multiple_stocks(body: StockBatch):
    results = []
    errors = []
    
    for ticker in body.tickers:
        try:
            data = scraper.scrape(ticker)
            stored = stock_repository.store(data["basic_info"])
            details = financial_info_repository.store(data["last_financial_info"], stored["id"])   
            market_values = market_values_repository.store(data["market_values"], stored["id"])
            variations = variations_repository.store(data["variations"], stored["id"])
            indicators = indicator_repository.store(data["indicators"], stored["id"])
            balance_sheets = balance_sheets_repository.store(data["balance_sheet"], stored["id"])
            financial_results = financial_results_repository.store(data["financial_results"], stored["id"])

            results.append({
                "ticker": ticker,
                "status": "success",
                "data": data
            })
        except Exception as e:
            errors.append({
                "ticker": ticker,
                "status": "error",
                "error": str(e)
            })
    
    return {
        "results": results,
        "errors": errors
    }
