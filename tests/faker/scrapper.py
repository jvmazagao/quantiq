from typing import Any

from faker.providers import BaseProvider


class StockProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        self.stocks_suffixes = ["3", "4", "11"]

    def ticker(self) -> str:
        stock_name = self.generator.unique.word()
        suffix = self.generator.random_element(elements=self.stocks_suffixes)
        return f"{stock_name}{suffix}"

    def name(self) -> str:
        return self.generator.unique.word()


class ReitProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        self.reits_suffixes = ["11"]

    def ticker(self) -> str:
        reit_name = self.generator.unique.word()
        suffix = self.generator.random_element(elements=self.reits_suffixes)
        return f"{reit_name}{suffix}"

    def name(self) -> str:
        return self.generator.unique.word()


class StockScrapperProvider(StockProvider):
    def stock_data(self) -> dict[str, Any]:
        stock_name = self.generator.unique.word()
        ticker = self.ticker()
        return {
            "ticker": ticker,
            "name": stock_name,
        }
