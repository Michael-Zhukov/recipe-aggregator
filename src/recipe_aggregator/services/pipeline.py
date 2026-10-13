from collections import Counter
from collections.abc import Iterable, Iterator

from ..domain.models import Recipe


def deduplicate(items: Iterable[Recipe]) -> Iterator[Recipe]:
    seen: set[tuple[str, str]] = set()

    for recipe in items:
        if recipe.key not in seen:
            seen.add(recipe.key)
            yield recipe


def count_by_ingredient(items: Iterable[Recipe]) -> Counter[str]:
    return Counter(recipe.main_ingredient for recipe in items)
