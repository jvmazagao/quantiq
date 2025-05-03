from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from quantiq.scraper import FundamentusScraper

app = FastAPI(
    title="Quantiq API",
    description="API for scraping stock data from Fundamentus",
    version="1.0.0"
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
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 