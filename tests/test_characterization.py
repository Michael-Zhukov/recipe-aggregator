from pathlib import Path

from recipe_aggregator.services.pipeline import load_recipes


def test_refactored_output_is_stable() -> None:
    recipes = load_recipes(Path("data/recipes.json"))

    assert len(recipes) == 10
    assert recipes[0].title == "борщ український"
    assert recipes[0].cooking_time == 90

    lentil_soup = next(recipe for recipe in recipes if recipe.title == "суп із сочевиці")

    assert lentil_soup.cooking_time is None
