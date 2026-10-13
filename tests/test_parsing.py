from recipe_aggregator.domain.parsing import (
    normalize_title,
    parse_cooking_time,
    to_recipe,
)


def test_normalize_title():
    assert normalize_title("  Борщ   Український  ") == "борщ український"


def test_parse_cooking_time():
    assert parse_cooking_time("90") == 90
    assert parse_cooking_time("невідомо") is None
    assert parse_cooking_time(None) is None


def test_to_recipe():
    row = {
        "title": " Борщ Український ",
        "category": "Супи",
        "cooking_time": "90",
        "main_ingredient": "Буряк",
    }

    recipe = to_recipe(row)

    assert recipe is not None
    assert recipe.title == "борщ український"
    assert recipe.cooking_time == 90


def test_empty_title():
    assert to_recipe({"title": ""}) is None


def test_parse_cooking_time_invalid_values():
    assert parse_cooking_time(True) is None
    assert parse_cooking_time(False) is None
    assert parse_cooking_time(-10) is None
    assert parse_cooking_time(0) == 0


def test_category_normalization():
    first = to_recipe(
        {
            "title": "Борщ",
            "category": "Супи",
        }
    )

    second = to_recipe(
        {
            "title": "Борщ",
            "category": " СУПИ ",
        }
    )

    assert first is not None
    assert second is not None
    assert first.category == second.category
    assert first.key == second.key
