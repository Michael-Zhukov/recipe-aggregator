from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path

from ..domain.models import Recipe
from ..domain.parsing import to_recipe
from ..sources.json_file import read_rows


def deduplicate(items: Iterable[Recipe]) -> Iterator[Recipe]:
    seen: set[tuple[str, str]] = set()

    for recipe in items:
        if recipe.key not in seen:
            seen.add(recipe.key)
            yield recipe


def count_by_ingredient(items: Iterable[Recipe]) -> Counter[str]:
    return Counter(recipe.main_ingredient for recipe in items)


def load_recipes(path: Path) -> list[Recipe]:
    rows = read_rows(path)
    parsed = (to_recipe(row) for row in rows)
    valid = (recipe for recipe in parsed if recipe is not None)
    return list(deduplicate(valid))


def test_load_recipes():
    recipes = load_recipes(Path("data/recipes.json"))

    assert len(recipes) == 10
    assert recipes[0].title == "борщ український"
    assert recipes[0].cooking_time == 90

    lentil_soup = next(recipe for recipe in recipes if recipe.title == "суп із сочевиці")
    assert lentil_soup.cooking_time is None
