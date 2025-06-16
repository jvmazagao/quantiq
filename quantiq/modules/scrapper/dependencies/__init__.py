from quantiq.modules.scrapper.providers.fundamentus.reit_extractor import (
    FundamentusREITScraper,
)
from quantiq.modules.scrapper.providers.fundamentus.stock_extractor import (
    FundamentusScraper,
)
from quantiq.modules.scrapper.strategies.extractor import ExtractorStrategy

__all__ = [
    "make_fundamentus_scraper",
    "make_fundamentus_reit_scraper",
    "make_extractor_strategy",
]


def make_fundamentus_scraper() -> FundamentusScraper:
    return FundamentusScraper()


def make_fundamentus_reit_scraper() -> FundamentusREITScraper:
    return FundamentusREITScraper()


def make_extractor_strategy() -> ExtractorStrategy:
    extractor_strategy = ExtractorStrategy()
    extractor_strategy.set_strategy(make_fundamentus_scraper())
    extractor_strategy.set_strategy(make_fundamentus_reit_scraper())
    return extractor_strategy
