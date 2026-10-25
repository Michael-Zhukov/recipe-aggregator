from collections.abc import Mapping

from .models import Recipe


def normalize_title(raw: str) -> str:
    return " ".join(raw.split()).lower()


def parse_cooking_time(raw: object) -> int | None:
    if isinstance(raw, bool):
        return None

    if not isinstance(raw, (str, int, float)):
        return None

    try:
        cooking_time = int(raw)
    except (TypeError, ValueError, OverflowError):
        return None

    return cooking_time if cooking_time >= 0 else None


def to_recipe(row: Mapping[str, object]) -> Recipe | None:
    title = row.get("title")
    category = row.get("category")

    if not isinstance(title, str) or not title.strip():
        return None

    if not isinstance(category, str) or not category.strip():
        return None

    ingredient = row.get("main_ingredient")
    if not isinstance(ingredient, str):
        ingredient = ""

    return Recipe(
        title=normalize_title(title),
        category=normalize_title(category),
        cooking_time=parse_cooking_time(row.get("cooking_time")),
        main_ingredient=ingredient,
    )
