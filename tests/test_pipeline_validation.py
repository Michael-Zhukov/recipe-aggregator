import pytest

from recipe_aggregator.domain.models import Recipe
from recipe_aggregator.services.pipeline import PipelineStats, parse_all
from recipe_aggregator.sources.schemas import RecipeIn


def test_pipeline_counts_invalid_records() -> None:
    rows: list[dict[str, object]] = [
        {
            "title": "Борщ",
            "category": "Супи",
            "cooking_time": 90,
        },
        {
            "title": "",
            "category": "Супи",
        },
        {
            "title": "Каша",
            "category": "",
        },
        {
            "title": "Салат",
            "category": "Салати",
            "cooking_time": "невідомо",
        },
    ]

    stats = PipelineStats()
    recipes = list(parse_all(rows, stats))

    assert stats.read == 4
    assert stats.invalid == 2
    assert len(recipes) == 2
    assert recipes[0].title == "борщ"
    assert recipes[1].cooking_time is None


def test_pipeline_handles_domain_value_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_to_domain = RecipeIn.to_domain

    def convert(self: RecipeIn) -> Recipe:
        if self.title == "поганий":
            raise ValueError("domain invariant")

        return original_to_domain(self)

    monkeypatch.setattr(RecipeIn, "to_domain", convert)

    rows: list[dict[str, object]] = [
        {"title": "Поганий", "category": "Супи"},
        {"title": "Борщ", "category": "Супи"},
    ]

    stats = PipelineStats()
    recipes = list(parse_all(rows, stats))

    assert stats.read == 2
    assert stats.invalid == 1
    assert len(recipes) == 1
    assert recipes[0].title == "борщ"
