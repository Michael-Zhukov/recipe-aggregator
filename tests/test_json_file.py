from pathlib import Path

from recipe_aggregator.sources.json_file import read_rows


def test_read_rows():
    path = Path("data/recipes.json")
    rows = list(read_rows(path))

    assert len(rows) == 12
    assert rows[0]["title"] == " Борщ Український "
    assert rows[0]["cooking_time"] == "90"
