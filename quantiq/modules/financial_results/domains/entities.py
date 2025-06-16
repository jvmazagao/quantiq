class FinancialResult:
    def __init__(self, stock_id: int, period: str, identifier: str, value: str) -> None:
        self.stock_id = stock_id
        self.period = period
        self.identifier = identifier
        self.value = value


class FinancialResults:
    def __init__(self, financial_results: list[FinancialResult]) -> None:
        self.financial_results = financial_results

    @staticmethod
    def parse(data: dict[str, dict[str, str]], stock_id: int) -> "FinancialResults":
        financial_results = []
        for period, values in data.items():
            for identifier, value in values.items():
                financial_result = FinancialResult(stock_id, period, identifier, value)
                financial_results.append(financial_result)
        return FinancialResults(financial_results)
