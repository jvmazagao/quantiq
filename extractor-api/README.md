# Quantiq

Quantiq is a FastAPI-based application that provides an API for scraping and storing Brazilian stock market data from Fundamentus, including both stocks and REITs (Real Estate Investment Trusts). The project follows Domain-Driven Design (DDD) principles and is organized into modules for better maintainability and scalability.

## Features

- Scrapes stock and REIT data from Fundamentus
- Stores comprehensive financial information including:
  - Basic asset information
  - Financial indicators
  - Market values
  - Price variations
  - Balance sheets
  - Financial results
- RESTful API endpoints for accessing and managing asset data
- Modular architecture following DDD principles
- Extensible scraping strategy pattern
- SQLite database for data persistence
- Comprehensive test coverage
- Code quality tools (Ruff, Pyright, Black, isort)

## API Endpoints

### GET /
Returns a welcome message and available endpoints.

### GET /assets/{ticker}
Retrieves and stores asset data for a given ticker (stocks or REITs).
- Parameters:
  - `ticker`: Asset ticker symbol (e.g., "PETR4", "XPML11")
- Returns: Complete asset data including financial information

## Setup

### Prerequisites
- Python 3.10 or higher
- Poetry (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd quantiq
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Run the application:
   ```bash
   poetry run uvicorn quantiq.main:app --reload
   ```

   Or use the Makefile for easier development:
   ```bash
   make setup  # First time setup
   make dev    # Start development server
   ```

The API will be available at `http://localhost:8000`

## Development

This project includes a comprehensive Makefile for common development tasks:

### Quick Start
```bash
make setup  # Install dependencies and setup pre-commit hooks
make dev    # Start development server
```

### Code Quality
```bash
make lint       # Check code quality
make lint-fix   # Fix code quality issues
make format     # Format code
make typecheck  # Run type checking
```

### Testing
```bash
make test       # Run tests
make test-cov   # Run tests with coverage report
```

### Combined Workflows
```bash
make fix        # Fix and format code
make check      # Run lint and typecheck
make ready      # Prepare code for commit (fix, typecheck, test)
make full-check # Run all validations
```

### Other Commands
```bash
make clean      # Clean up cache files
make update     # Update dependencies
make status     # Show project status
```

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
quantiq/
├── quantiq/
│   ├── main.py                    # FastAPI application entry point
│   ├── core/                      # Core infrastructure
│   │   ├── domain/               # Base domain classes
│   │   ├── errors/               # Error handling
│   │   ├── infra/                # Infrastructure layer
│   │   │   ├── databases/        # Database configurations
│   │   │   └── tables.py         # Database table definitions
│   │   ├── logging/              # Logging configuration
│   │   ├── repositories/         # Base repository classes
│   │   └── utils/                # Utility functions
│   └── modules/
│       ├── assets/               # Assets module (stocks & REITs)
│       │   ├── controllers/      # API controllers
│       │   ├── domains/          # Domain entities and value objects
│       │   ├── manager/          # Business logic managers
│       │   ├── repositories/     # Data access layer
│       │   └── services/         # Application services
│       └── scrapper/             # Web scraping module
│           ├── providers/        # Data providers (Fundamentus)
│           │   └── fundamentus/  # Fundamentus-specific scrapers
│           │       ├── extractor/ # Stock and REIT extractors
│           │       └── data/     # Data models
│           └── strategies/       # Scraping strategy pattern
├── tests/                        # Test suite
├── pyproject.toml               # Project configuration and dependencies
├── poetry.lock                  # Locked dependencies
├── Makefile                     # Development commands
└── README.md                    # This file
```

## Architecture

The project follows Domain-Driven Design principles with a clear separation of concerns:

- **Domain Layer**: Contains business entities and value objects
- **Application Layer**: Implements services and managers that orchestrate domain objects
- **Infrastructure Layer**: Handles data persistence and external services
- **Presentation Layer**: Exposes REST API endpoints through controllers

Each module is self-contained with its own:
- Domain entities
- Repositories
- Services
- Controllers

## Development Tools

- **Poetry**: Dependency management and packaging
- **Ruff**: Fast Python linter and formatter
- **Pyright**: Static type checker
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks for code quality
- **Black**: Code formatter
- **isort**: Import sorting

## Testing

The project includes comprehensive tests with coverage reporting:

```bash
make test-cov  # Run tests with coverage
```

Coverage reports are generated in the `htmlcov/` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
