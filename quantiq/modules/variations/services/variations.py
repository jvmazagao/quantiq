from quantiq.modules.variations.repositories.variations import VariationsRepository
from quantiq.modules.variations.domains.entities import Variations

class VariationsService:
    def __init__(self, variations_repository: VariationsRepository):
        self.variations_repository = variations_repository

    def store(self, variations: dict, stock_id: int):
        variations = Variations.parse(variations, stock_id)
        stored_variations = self.variations_repository.store(variations)
        return stored_variations

    def fetch(self, stock_id: int) -> Variations | None:
        return self.variations_repository.fetch(stock_id)