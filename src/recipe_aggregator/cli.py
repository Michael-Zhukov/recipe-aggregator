import argparse
from pathlib import Path

from .services.pipeline import count_by_ingredient, load_recipes


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="recipe-aggregator",
        description="Агрегатор рецептів та аналіз інгредієнтів",
    )

    parser.add_argument(
        "path",
        type=Path,
        help="Шлях до JSON-файлу з рецептами",
    )

    args = parser.parse_args()

    recipes = load_recipes(args.path)

    print(f"Завантажено унікальних рецептів: {len(recipes)}")
    print("Статистика основних інгредієнтів:")

    for ingredient, count in count_by_ingredient(recipes).most_common():
        print(f"  {ingredient}: {count}")


if __name__ == "__main__":
    main()
