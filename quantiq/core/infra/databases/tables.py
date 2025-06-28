tables = {
    "assets": """
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE,
            name TEXT,
            type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """,
    "asset_details": """
        CREATE TABLE IF NOT EXISTS asset_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            governance TEXT,
            sector TEXT,
            subsector TEXT,
            market_value INTEGER,
            last_balance_proccessed DATETIME,
            company_value INTEGER,
            number_of_stocks INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (asset_id) REFERENCES assets (id)
        );
    """,
}
