class BalanceSheet:
    def __init__(self, stock_id, identifier, value):
        self.stock_id = stock_id
        self.identifier = identifier
        self.value = value

class BalanceSheets:
    def __init__(self, balance_sheets):
        self.balance_sheets = balance_sheets

    @staticmethod
    def parse(data, stock_id):
        balance_sheets = []
        for identifier, value in data.items():
            balance_sheets.append(BalanceSheet(stock_id, identifier, value))
        return BalanceSheets(balance_sheets)