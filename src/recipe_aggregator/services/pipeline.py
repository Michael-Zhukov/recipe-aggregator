from collections import Counter
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from ..domain.models import Recipe
from ..domain.parsing import to_recipe
from ..sources.json_file import read_rows
from ..sources.schemas import RecipeIn


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0

    by_category: Counter[str] = field(default_factory=Counter)

    cooking_time_count: int = 0
    cooking_time_sum: int = 0
    cooking_time_min: int | None = None
    cooking_time_max: int | None = None

    @property
    def cooking_time_avg(self) -> float | None:
        if self.cooking_time_count == 0:
            return None

        return self.cooking_time_sum / self.cooking_time_count


def parse_all(
    rows: Iterable[Mapping[str, object]],
    stats: PipelineStats,
) -> Iterator[Recipe]:
    for row in rows:
        stats.read += 1

        try:
            recipe = RecipeIn.model_validate(row).to_domain()
        except ValidationError:
            stats.invalid += 1
            continue

        yield recipe


def deduplicate(
    items: Iterable[Recipe],
    stats: PipelineStats | None = None,
) -> Iterator[Recipe]:
    seen: set[tuple[str, str]] = set()

    for recipe in items:
        if recipe.key in seen:
            if stats is not None:
                stats.duplicates += 1
            continue

        seen.add(recipe.key)
        yield recipe


def collect(
    items: Iterable[Recipe],
    stats: PipelineStats,
) -> None:
    for recipe in items:
        stats.kept += 1
        stats.by_category[recipe.category] += 1

        cooking_time = recipe.cooking_time

        if cooking_time is None:
            continue

        stats.cooking_time_count += 1
        stats.cooking_time_sum += cooking_time

        if stats.cooking_time_min is None or cooking_time < stats.cooking_time_min:
            stats.cooking_time_min = cooking_time

        if stats.cooking_time_max is None or cooking_time > stats.cooking_time_max:
            stats.cooking_time_max = cooking_time


def count_by_ingredient(items: Iterable[Recipe]) -> Counter[str]:
    return Counter(recipe.main_ingredient for recipe in items)


def load_recipes(path: Path) -> list[Recipe]:
    rows = read_rows(path)
    parsed = (to_recipe(row) for row in rows)
    valid = (recipe for recipe in parsed if recipe is not None)
    return list(deduplicate(valid))


def test_load_recipes() -> None:
    recipes = load_recipes(Path("data/recipes.json"))

    assert len(recipes) == 10
    assert recipes[0].title == "борщ український"
    assert recipes[0].cooking_time == 90

    lentil_soup = next(recipe for recipe in recipes if recipe.title == "суп із сочевиці")
    assert lentil_soup.cooking_time is None
