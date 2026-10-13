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


def to_recipe(row: dict) -> Recipe | None:
    title = row.get("title") or ""

    if not title.strip():
        return None

    return Recipe(
        title=normalize_title(title),
        category=normalize_title(row.get("category") or ""),
        cooking_time=parse_cooking_time(row.get("cooking_time")),
        main_ingredient=row.get("main_ingredient", ""),
    )
