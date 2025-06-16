from abc import ABC, abstractmethod
from typing import Any


class Scrapper(ABC):
    type: str

    def __init__(self, type: str) -> None:
        self.type = type

    @abstractmethod
    def scrape(self, ticker: str) -> dict[str, Any]:
        pass
