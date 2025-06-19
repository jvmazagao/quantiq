from faker import Faker
from pytest import fixture

from quantiq.modules.scrapper.providers.fundamentus.data import (
    Variations,
    YearlyVariation,
)


class TestVariations:
    @fixture
    def fake(self) -> Faker:
        return Faker()

    @fixture
    def data(self, fake: Faker) -> dict[str, float]:
        return {
            "dia": fake.pyfloat(right_digits=2),
            "mes": fake.pyfloat(right_digits=2),
            "30_dias": fake.pyfloat(right_digits=2),
            "12_meses": fake.pyfloat(right_digits=2),
        }

    @fixture
    def dynamic_data(self, fake: Faker) -> dict[str, float | None]:
        return {
            "dia": fake.pyfloat(right_digits=2),
            "mes": fake.pyfloat(right_digits=2),
            "30_dias": fake.pyfloat(right_digits=2),
            "12_meses": fake.pyfloat(right_digits=2),
            "2025": fake.pyfloat(right_digits=2),
            "2024": fake.pyfloat(right_digits=2),
            "2023": fake.pyfloat(right_digits=2),
            "2022": None,
            "2021": fake.pyfloat(right_digits=2),
            "2020": fake.pyfloat(right_digits=2),
        }

    def test_basic_variations(self, data: dict[str, float]):
        variations = Variations.create(data)
        assert variations.day == data["dia"]
        assert variations.month == data["mes"]
        assert variations.thirty_days == data["30_dias"]
        assert variations.twelve_months == data["12_meses"]

    def test_variations_dynamic_fields(self, dynamic_data: dict[str, float]):
        variations = Variations.create(dynamic_data)
        assert variations.day == dynamic_data["dia"]
        assert variations.month == dynamic_data["mes"]
        assert variations.thirty_days == dynamic_data["30_dias"]
        assert variations.twelve_months == dynamic_data["12_meses"]
        assert variations.yearly_variations == [
            YearlyVariation(year=2025, variation=dynamic_data["2025"]),
            YearlyVariation(year=2024, variation=dynamic_data["2024"]),
            YearlyVariation(year=2023, variation=dynamic_data["2023"]),
            YearlyVariation(year=2022, variation=None),
            YearlyVariation(year=2021, variation=dynamic_data["2021"]),
            YearlyVariation(year=2020, variation=dynamic_data["2020"]),
        ]

    def test_variations_invalid_year(self, data: dict[str, float | None]):
        data["2025"] = "invalid"  # type: ignore
        variations = Variations.create(data)
        assert variations.yearly_variations == []

    def test_variations_invalid_variation(self, data: dict[str, float | None]):
        data["1888"] = None  # type: ignore
        variations = Variations.create(data)
        assert variations.yearly_variations == []
