from .models import Recipe


def normalize_title(raw: str) -> str:
    return " ".join(raw.split()).lower()


def parse_cooking_time(raw: object) -> int | None:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def to_recipe(row: dict) -> Recipe | None:
    title = row.get("title") or ""

    if not title.strip():
        return None

    return Recipe(
        title=normalize_title(title),
        category=row.get("category", ""),
        cooking_time=parse_cooking_time(row.get("cooking_time")),
        main_ingredient=row.get("main_ingredient", ""),
    )
