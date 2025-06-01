class Stock:
    def __init__(self, ticker: str, type: str, name: str, sector: str, subsector: str, id: int = None):
        self.id = id
        self.ticker = ticker
        self.type = type
        self.name = name
        self.sector = sector
        self.subsector = subsector
    
    @staticmethod
    def parse(data: dict):
        return Stock(
            ticker=data["papel"],
            type=data["tipo"],
            name=data["empresa"],
            sector=data["setor"],
            subsector=data["subsetor"]
        )