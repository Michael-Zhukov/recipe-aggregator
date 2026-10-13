import time
import tracemalloc
from pathlib import Path

from recipe_aggregator.domain.parsing import to_recipe
from recipe_aggregator.services.pipeline import (
    PipelineStats,
    collect,
    deduplicate,
    parse_all,
)
from recipe_aggregator.sources.json_file import read_rows_jsonl

PATH = Path("data/large.jsonl")


def lazy() -> int:
    stats = PipelineStats()

    rows = read_rows_jsonl(PATH)
    parsed = parse_all(rows, stats)
    unique = deduplicate(parsed, stats)
    collect(unique, stats)

    return stats.kept


def greedy() -> int:
    rows = list(read_rows_jsonl(PATH))
    parsed = [to_recipe(row) for row in rows]
    valid = [recipe for recipe in parsed if recipe is not None]

    seen: set[tuple[str, str]] = set()
    unique = []

    for recipe in valid:
        if recipe.key not in seen:
            seen.add(recipe.key)
            unique.append(recipe)

    return len(unique)


def main() -> None:
    for name, function in (
        ("Генераторний конвеєр", lazy),
        ("Проміжні списки", greedy),
    ):
        tracemalloc.start()
        start = time.perf_counter()

        count = function()

        elapsed = time.perf_counter() - start
        peak = tracemalloc.get_traced_memory()[1] / 1024 / 1024
        tracemalloc.stop()

        print(f"{name:22} {count} рецептів {elapsed:.2f} с пік {peak:.1f} МБ")


if __name__ == "__main__":
    main()
