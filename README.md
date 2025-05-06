# Quantiq

Quantiq is a FastAPI-based application that provides an API for scraping and storing stock market data from Fundamentus, a Brazilian financial data provider.

## Features

- Scrapes stock data from Fundamentus
- Stores comprehensive financial information including:
  - Basic stock information
  - Financial indicators
  - Market values
  - Price variations
  - Balance sheets
  - Financial results
- RESTful API endpoints for accessing and managing stock data

## API Endpoints

### GET /
Returns a welcome message and available endpoints.

### GET /stocks/{ticker}
Retrieves and stores stock data for a given ticker.
- Parameters:
  - `ticker`: Stock ticker symbol (e.g., "PETR4")
- Returns: Complete stock data including financial information

### DELETE /stocks/{ticker}
Removes stock data for a given ticker.
- Parameters:
  - `ticker`: Stock ticker symbol to be removed

### POST /stocks/batch
Retrieves and stores stock data for multiple tickers in a single request.
- Parameters:
  - `tickers`: List of stock ticker symbols (e.g., ["PETR4", "VALE3", "ITUB4"])
- Returns: 
  - `results`: List of successfully processed stocks with their data
  - `errors`: List of stocks that failed to process with error messages

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn quantiq.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
quantiq/
├── main.py                 # FastAPI application and routes
├── scraper.py              # Fundamentus scraper implementation
├── database/
│   └── database.py         # Database configuration
└── repositories/
    ├── stock_repository.py
    ├── financial_info_repository.py
    ├── market_values_repository.py
    ├── variations_repository.py
    ├── indicator_repository.py
    ├── balance_sheets_repository.py
    └── financial_results_repository.py
```

## License

This project is licensed under the Non-Commercial Use Only License (NCUL). See the [LICENSE](LICENSE) file for details.
