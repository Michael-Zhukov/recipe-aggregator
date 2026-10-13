from itertools import batched
from pathlib import Path

from recipe_aggregator.services.pipeline import (
    PipelineStats,
    deduplicate,
    parse_all,
)
from recipe_aggregator.sources.json_file import read_rows_jsonl


def main() -> None:
    stats = PipelineStats()

    rows = read_rows_jsonl(Path("data/large.jsonl"))
    parsed = parse_all(rows, stats)
    unique = deduplicate(parsed, stats)

    batch_count = 0

    for batch in batched(unique, 500):
        batch_count += 1
        stats.kept += len(batch)

    print(f"Прочитано: {stats.read}")
    print(f"Некоректних: {stats.invalid}")
    print(f"Дублікатів: {stats.duplicates}")
    print(f"Унікальних: {stats.kept}")
    print(f"Пакетів по 500: {batch_count}")


if __name__ == "__main__":
    main()
