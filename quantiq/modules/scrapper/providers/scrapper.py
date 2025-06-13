from abc import ABC, abstractmethod

class Scrapper(ABC):
    type: str
    
    def __init__(self, type: str):
        self.type = type
    
    @abstractmethod
    def scrape(self, ticker: str):
        pass
    