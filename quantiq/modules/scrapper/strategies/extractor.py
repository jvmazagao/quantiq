from typing import Any

from quantiq.modules.scrapper.providers.scrapper import Scrapper


class ExtractorStrategy:
    strategy: set[tuple[str, Scrapper]] = set()

    def set_strategy(self, strategy: Scrapper) -> None:
        self.strategy.add((strategy.type, strategy))

    def execute(self, type: str, ticker: str) -> dict[str, Any]:
        for scrapper_type, scrapper in self.strategy:
            if scrapper_type == type:
                return scrapper.scrape(ticker)

        raise ValueError(f"Invalid type: {type}")
