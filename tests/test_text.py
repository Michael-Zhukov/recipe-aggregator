from recipe_aggregator.text import normalize_title


def test_normalize_title() -> None:
    assert normalize_title("  Chicken   Pasta  ") == "chicken pasta"


def test_normalize_title_removes_extra_spaces() -> None:
    assert normalize_title("Tomato    Soup") == "tomato soup"


def test_normalize_title_handles_empty_string() -> None:
    assert normalize_title("") == ""
