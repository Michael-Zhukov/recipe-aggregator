from dataclasses import FrozenInstanceError

import pytest

from recipe_aggregator.domain.models import Recipe


@pytest.mark.parametrize(
    "title, category, cooking_time, main_ingredient",
    [
        (" ", "Soup", 30, "Potato"),
        ("Borsch", "", 60, "Beet"),
        ("Borsch", "Soup", -5, "Beet"),
        ("Borsch", "Soup", True, "Beet"),
    ],
)
def test_invalid_recipe_rejected(
    title: str,
    category: str,
    cooking_time: int | None,
    main_ingredient: str,
) -> None:
    with pytest.raises(ValueError):
        Recipe(title, category, cooking_time, main_ingredient)


def test_frozen_model_is_hashable() -> None:
    a = Recipe("Borsch", "Soup", 60, "Beet")
    b = Recipe("Borsch", "Soup", 60, "Beet")

    assert len({a, b}) == 1


def test_recipe_is_immutable() -> None:
    recipe = Recipe("Borsch", "Soup", 60, "Beet")
    field_name = "title"

    with pytest.raises(FrozenInstanceError):
        setattr(recipe, field_name, "New title")


def test_unknown_cooking_time_allowed() -> None:
    recipe = Recipe("Borsch", "Soup", None, "Beet")

    assert recipe.cooking_time is None


def test_unknown_main_ingredient_allowed() -> None:
    recipe = Recipe("Borsch", "Soup", 60, "")

    assert recipe.main_ingredient == ""
