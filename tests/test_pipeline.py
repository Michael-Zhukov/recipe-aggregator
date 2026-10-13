from itertools import batched
from pathlib import Path

from recipe_aggregator.domain.models import Recipe
from recipe_aggregator.services.pipeline import (
    PipelineStats,
    collect,
    count_by_ingredient,
    deduplicate,
    load_recipes,
    parse_all,
)


def test_deduplicate():
    recipes = [
        Recipe("борщ", "Супи", 90, "Буряк"),
        Recipe("борщ", "Супи", 100, "Буряк"),
        Recipe("сирники", "Сніданки", 25, "Сир"),
    ]

    result = list(deduplicate(recipes))

    assert len(result) == 2
    assert result[0].title == "борщ"
    assert result[0].cooking_time == 90
    assert result[1].title == "сирники"


def test_count_by_ingredient():
    recipes = [
        Recipe("борщ", "Супи", 90, "Буряк"),
        Recipe("салат", "Салати", 15, "Картопля"),
        Recipe("пюре", "Гарніри", 30, "Картопля"),
    ]

    statistics = count_by_ingredient(recipes)

    assert statistics["Картопля"] == 2
    assert statistics["Буряк"] == 1
    assert statistics["Морква"] == 0


def test_load_recipes():
    recipes = load_recipes(Path("data/recipes.json"))

    assert len(recipes) == 10
    assert recipes[0].title == "борщ український"
    assert recipes[0].cooking_time == 90

    lentil_soup = next(recipe for recipe in recipes if recipe.title == "суп із сочевиці")

    assert lentil_soup.cooking_time is None


def test_invalid_rows_are_counted():
    rows = [
        {
            "title": "Борщ",
            "category": "Супи",
            "cooking_time": "90",
            "main_ingredient": "Буряк",
        },
        {
            "title": "",
            "category": "Салати",
            "cooking_time": "20",
            "main_ingredient": "Огірок",
        },
    ]

    stats = PipelineStats()
    result = list(parse_all(rows, stats))

    assert len(result) == 1
    assert stats.read == 2
    assert stats.invalid == 1


def test_duplicates_are_counted():
    rows = [
        {
            "title": "Борщ",
            "category": "Супи",
            "cooking_time": "90",
            "main_ingredient": "Буряк",
        },
        {
            "title": "Борщ",
            "category": "Супи",
            "cooking_time": "90",
            "main_ingredient": "Буряк",
        },
    ]

    stats = PipelineStats()
    result = list(deduplicate(parse_all(rows, stats), stats))

    assert len(result) == 1
    assert stats.duplicates == 1


def test_collect_statistics():
    rows = [
        {
            "title": "Борщ",
            "category": "Супи",
            "cooking_time": "90",
            "main_ingredient": "Буряк",
        },
        {
            "title": "Салат",
            "category": "Салати",
            "cooking_time": "20",
            "main_ingredient": "Огірок",
        },
    ]

    stats = PipelineStats()
    collect(parse_all(rows, stats), stats)

    assert stats.kept == 2
    assert stats.cooking_time_min == 20
    assert stats.cooking_time_max == 90
    assert stats.cooking_time_avg == 55


def test_batched_splits_tail():
    assert [len(batch) for batch in batched(range(7), 3)] == [3, 3, 1]
