# quantiq

A FastAPI server that scrapes and returns all structured data from the Fundamentus BBAS3 page.

## Setup

1. Install dependencies (if not already):

```bash
poetry install
```

2. Run the FastAPI server:

```bash
poetry run uvicorn quantiq.main:app --reload
```

3. Access the data at:

- [http://localhost:8000/bbas3](http://localhost:8000/bbas3)
