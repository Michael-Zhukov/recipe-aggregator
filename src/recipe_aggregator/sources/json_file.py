import json
from collections.abc import Iterator
from pathlib import Path


def _as_row(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None

    row: dict[str, object] = {}

    for key, item in value.items():
        if not isinstance(key, str):
            return None
        row[key] = item

    return row


def read_rows(path: Path) -> Iterator[dict[str, object]]:
    with path.open(encoding="utf-8") as file:
        data: object = json.load(file)

    if not isinstance(data, list):
        return

    for item in data:
        row = _as_row(item)

        if row is not None:
            yield row


def read_rows_jsonl(path: Path) -> Iterator[dict[str, object]]:
    with path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            try:
                data: object = json.loads(line)
            except json.JSONDecodeError:
                continue

            row = _as_row(data)

            if row is not None:
                yield row
