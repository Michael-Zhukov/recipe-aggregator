import time
import tracemalloc
from pathlib import Path

from recipe_aggregator.sources.json_file import read_rows_jsonl


def measure(lazy: bool, path: Path) -> None:
    tracemalloc.start()
    start = time.perf_counter()

    if lazy:
        rows = read_rows_jsonl(path)
    else:
        rows = list(read_rows_jsonl(path))

    total = sum(1 for _ in rows)

    elapsed = time.perf_counter() - start
    peak = tracemalloc.get_traced_memory()[1] / 1024 / 1024

    tracemalloc.stop()

    mode = "Генератор" if lazy else "Список"

    print(f"{mode}: {total} записів, {elapsed:.2f} с, пік {peak:.1f} МБ")


def main() -> None:
    path = Path("data/large.jsonl")

    measure(lazy=True, path=path)
    measure(lazy=False, path=path)


if __name__ == "__main__":
    main()
