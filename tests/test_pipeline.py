from pathlib import Path

from recipe_aggregator.domain.models import Recipe
from recipe_aggregator.services.pipeline import (
    count_by_ingredient,
    deduplicate,
    load_recipes,
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
