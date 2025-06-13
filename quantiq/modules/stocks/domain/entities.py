class Stock:
    def __init__(self, ticker: str, type: str, name: str, sector: str = None, subsector: str = None, id: int = None):
        self.id = id
        self.ticker = ticker
        self.type = type
        self.name = name
        self.sector = sector
        self.subsector = subsector
    
    @staticmethod
    def parse(data: dict):   
        if not data:
            return None
            
        if "fii" in data: 
            return Stock(
                ticker=data.get("fii"),
                type=data.get("tipo"),
                name=data.get("nome"),
                sector=data.get("segmento")
            )
            
        return Stock(
            ticker=data.get("papel"),
            type=data.get("tipo"),
            name=data.get("empresa"),
            sector=data.get("setor"),
            subsector=data.get("subsetor")
        )