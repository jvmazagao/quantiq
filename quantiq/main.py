from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from quantiq.database.database import create_database
from quantiq.modules.stocks.dependencies import make_stock_router

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


@app.on_event("startup")
async def startup_event():
    create_database()
    logger.info("Database initialized")
    app.include_router(make_stock_router())

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
