import argparse
from itertools import batched, islice
from pathlib import Path

from .services.pipeline import (
    PipelineStats,
    collect,
    count_by_ingredient,
    deduplicate,
    load_recipes,
    parse_all,
)
from .sources.json_file import read_rows_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="recipe-aggregator",
        description="Агрегатор рецептів та аналіз інгредієнтів",
    )

    parser.add_argument(
        "path",
        type=Path,
        help="Шлях до JSON або JSONL-файлу з рецептами",
    )

    parser.add_argument(
        "--preview",
        type=int,
        metavar="N",
        help="Показати перші N рецептів",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Показати статистику обробки",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        metavar="N",
        help="Обробляти рецепти пакетами по N",
    )

    args = parser.parse_args()

    if args.preview is not None and args.preview < 0:
        parser.error("--preview має бути невід'ємним числом")

    if args.batch_size is not None and args.batch_size <= 0:
        parser.error("--batch-size має бути додатним числом")

    # Зберігаємо попередню поведінку для звичайного JSON.
    if args.path.suffix.lower() != ".jsonl":
        if args.preview is not None or args.stats or args.batch_size is not None:
            parser.error("Нові параметри підтримуються для JSONL-файлів")

        recipes = load_recipes(args.path)

        print(f"Завантажено унікальних рецептів: {len(recipes)}")
        print("Статистика основних інгредієнтів:")

        for ingredient, count in count_by_ingredient(recipes).most_common():
            print(f"  {ingredient}: {count}")

        return

    stats = PipelineStats()

    rows = read_rows_jsonl(args.path)
    parsed = parse_all(rows, stats)
    pipeline = deduplicate(parsed, stats)

    # Попередній перегляд без читання всього файлу.
    if args.preview is not None:
        for recipe in islice(pipeline, args.preview):
            print(recipe)

        print(f"Прочитано рядків: {stats.read}")
        return

    # Пакетна обробка.
    if args.batch_size is not None:
        batch_count = 0

        for batch in batched(pipeline, args.batch_size):
            batch_count += 1
            collect(batch, stats)

        print(f"Пакетів по {args.batch_size}: {batch_count}")
    else:
        collect(pipeline, stats)

    if args.stats:
        print(f"Прочитано записів: {stats.read}")
        print(f"Відхилено: {stats.invalid}")
        print(f"Дублікатів: {stats.duplicates}")
        print(f"Унікальних рецептів: {stats.kept}")

        print("Статистика за категоріями:")
        for category, count in stats.by_category.most_common():
            print(f"  {category}: {count}")

        if stats.cooking_time_count:
            print(
                "Час приготування: "
                f"min={stats.cooking_time_min}, "
                f"max={stats.cooking_time_max}, "
                f"avg={stats.cooking_time_avg:.2f} хв"
            )


if __name__ == "__main__":
    main()
