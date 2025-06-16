# Quantiq

Quantiq is a FastAPI-based application that provides an API for scraping and storing stock market data from Fundamentus, a Brazilian financial data provider. The project follows Domain-Driven Design (DDD) principles and is organized into modules for better maintainability and scalability.

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
- Modular architecture following DDD principles
- Extensible scraping strategy pattern

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
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
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
├── main.py                    # FastAPI application entry point
├── modules/
│   ├── stocks/               # Stocks module
│   │   ├── domain/          # Domain entities and value objects
│   │   ├── repositories/    # Data access layer
│   │   └── use_cases/      # Application business logic
│   ├── balance_sheet/       # Balance sheet module
│   ├── financial_info/      # Financial information module
│   ├── market_values/       # Market values module
│   ├── variations/          # Price variations module
│   ├── indicators/          # Financial indicators module
│   ├── financial_results/   # Financial results module
│   └── scrapper/           # Web scraping module
│       ├── strategies/     # Different scraping strategies
│       └── dependencies.py # Dependency injection
├── database/
│   └── database.py         # Database configuration
└── requirements.txt        # Project dependencies
```

## Architecture

The project follows Domain-Driven Design principles with a clear separation of concerns:

- **Domain Layer**: Contains business entities and value objects
- **Application Layer**: Implements use cases and orchestrates domain objects
- **Infrastructure Layer**: Handles data persistence and external services
- **Presentation Layer**: Exposes REST API endpoints

Each module is self-contained with its own:
- Domain entities
- Repositories
- Services
- Use cases

## License

This project is licensed under the Non-Commercial Use Only License (NCUL). See the [LICENSE](LICENSE) file for details.
