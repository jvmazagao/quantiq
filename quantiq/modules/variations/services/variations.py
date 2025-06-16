from quantiq.modules.variations.domains.entities import Variations
from quantiq.modules.variations.repositories.variations import VariationsRepository


class VariationsService:
    def __init__(self, variations_repository: VariationsRepository):
        self.variations_repository = variations_repository

    def store(self, data: dict[str, float | int], stock_id: int) -> Variations:
        variations = Variations.parse(data, stock_id)
        self.variations_repository.store(variations)

        return variations

    def fetch(self, stock_id: int) -> Variations:
        return self.variations_repository.fetch(stock_id)
