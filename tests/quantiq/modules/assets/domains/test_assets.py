from typing import Any

from faker import Faker
from pytest import fixture

from quantiq.modules.assets.domains.assets import Asset


class TestAssets:
    @fixture
    def data(self, fake: Faker) -> dict[str, Any]:
        return {
            "ticker": "".join(
                fake.company().upper().split(" ")[0]
                + str(fake.random_int(min=3, max=11))
            ),
            "type": "stock",
            "name": fake.company(),
        }

    def test_create_asset(self, data: dict[str, Any]):
        asset = Asset.create(data)
        assert asset.ticker == data["ticker"]
        assert asset.type.value == data["type"]
        assert asset.name == data["name"]
        assert asset.id is None
        assert asset.created_at is None
        assert asset.updated_at is None
