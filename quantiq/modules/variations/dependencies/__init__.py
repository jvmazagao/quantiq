from quantiq.modules.variations.repositories.variations import VariationsRepository
from quantiq.modules.variations.services.variations import VariationsService

__all__ = ["make_variations_service"]


def make_variations_repository() -> VariationsRepository:
    return VariationsRepository()


def make_variations_service() -> VariationsService:
    return VariationsService(make_variations_repository())
