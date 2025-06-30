from unittest.mock import MagicMock, Mock

from faker import Faker
from pytest import fixture
from pytest_mock import MockerFixture

from quantiq.core.infra.databases.sqlite.sqlite import Sqlite
from tests.faker.quantiq import AssetFaker
from tests.faker.scrapper import StockScrapperProvider


@fixture
def fake() -> Faker:
    faker = Faker()
    faker.add_provider(StockScrapperProvider(faker))
    faker.add_provider(AssetFaker(faker))
    return faker


@fixture
def mock_db(mocker: MockerFixture) -> Mock:
    mock_db = Mock(spec=Sqlite)
    mock_db.fetch_one.return_value = None
    mock_db.fetch_all.return_value = []
    mock_db.upsert.return_value = None
    mock_transaction = MagicMock()
    mock_transaction.__enter__.return_value = Mock()
    mock_transaction.__exit__.return_value = None
    mock_db.transaction.return_value = mock_transaction
    mocker.patch(
        "quantiq.core.infra.databases.sqlite.sqlite.Sqlite", return_value=mock_db
    )

    return mock_db
