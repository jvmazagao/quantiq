from faker import Faker
from pytest import fixture

from tests.faker.scrapper import StockScrapperProvider


@fixture
def fake() -> Faker:
    faker = Faker()
    faker.add_provider(StockScrapperProvider(faker))
    return faker
