from quantiq.modules.scrapper.providers.scrapper import Scrapper

class ExtractorStrategy:
    strategy: set[tuple[str, Scrapper]] = set()

    def set_strategy(self, strategy: Scrapper):
        self.strategy.add((strategy.type, strategy))
        
    def execute(self, type: str, ticker: str):
        for scrapper_type, scrapper in self.strategy:
            if scrapper_type == type:
                return scrapper.scrape(ticker)
            
        raise ValueError(f"Invalid type: {type}")
    

    
