class BalanceSheet:
    def __init__(self, stock_id: int, identifier: str, value: str) -> None:
        self.stock_id = stock_id
        self.identifier = identifier
        self.value = value


class BalanceSheets:
    def __init__(self, balance_sheets: list[BalanceSheet]) -> None:
        self.balance_sheets = balance_sheets

    @staticmethod
    def parse(data: dict[str, str], stock_id: int) -> "BalanceSheets":
        balance_sheets = []
        for identifier, value in data.items():
            balance_sheets.append(BalanceSheet(stock_id, identifier, value))
        return BalanceSheets(balance_sheets)
