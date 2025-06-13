from quantiq.modules.scrapper.providers.fundamentus.stock_extractor import FundamentusScraper
from quantiq.modules.scrapper.providers.fundamentus.reit_extractor import FundamentusREITScraper

__all__ = ["make_fundamentus_scraper", "make_fundamentus_reit_scraper"]

def make_fundamentus_scraper():
    return FundamentusScraper()

def make_fundamentus_reit_scraper():
    return FundamentusREITScraper()