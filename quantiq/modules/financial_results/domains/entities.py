class FinancialResult:
    def __init__(self, stock_id: int, period: str, identifier: str, value: str):
        self.stock_id = stock_id
        self.period = period
        self.identifier = identifier
        self.value = value


class FinancialResults:
    def __init__(self, financial_results: list[FinancialResult]):
        self.financial_results = financial_results

    @staticmethod
    def parse(data: dict, stock_id: int):
        financial_results = []
        for period, values in data.items():
            for identifier, value in values.items():
                financial_result = FinancialResult(stock_id, period, identifier, value)
                financial_results.append(financial_result)
        return FinancialResults(financial_results) 