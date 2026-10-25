import pytest
from pydantic import ValidationError

from recipe_aggregator.sources.schemas import RecipeIn


def test_recipe_in_normalization() -> None:
    data = {
        "title": "  Борщ   Український  ",
        "category": "  Супи  ",
        "cooking_time": "90",
        "main_ingredient": "Буряк",
    }

    recipe = RecipeIn.model_validate(data)

    assert recipe.title == "борщ український"
    assert recipe.category == "супи"
    assert recipe.cooking_time == 90


def test_unknown_cooking_time() -> None:
    recipe = RecipeIn.model_validate(
        {
            "title": "Суп",
            "category": "Супи",
            "cooking_time": "невідомо",
        }
    )

    assert recipe.cooking_time is None
    assert recipe.main_ingredient == ""


@pytest.mark.parametrize(
    "title, category",
    [
        ("", "Супи"),
        ("   ", "Супи"),
        ("Борщ", ""),
        ("Борщ", "   "),
    ],
)
def test_invalid_recipe_in(
    title: str,
    category: str,
) -> None:
    with pytest.raises(ValidationError):
        RecipeIn.model_validate(
            {
                "title": title,
                "category": category,
            }
        )


def test_to_domain() -> None:
    recipe_in = RecipeIn(
        title="Борщ",
        category="Супи",
        cooking_time=60,
        main_ingredient="Буряк",
    )

    recipe = recipe_in.to_domain()

    assert recipe.title == "борщ"
    assert recipe.category == "супи"
    assert recipe.cooking_time == 60
