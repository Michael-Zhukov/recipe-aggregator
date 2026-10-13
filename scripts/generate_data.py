import json
import random
from pathlib import Path


def main() -> None:
    ingredients = [
        "Картопля",
        "Буряк",
        "Морква",
        "Рис",
        "Гречка",
        "Борошно",
        "Сир",
        "Яблуко",
    ]

    categories = [
        "Супи",
        "Основні страви",
        "Салати",
        "Десерти",
    ]

    path = Path("data/large.jsonl")

    with path.open("w", encoding="utf-8") as file:
        for i in range(200_000):
            recipe = {
                "title": f"Рецепт {i % 500}",
                "category": random.choice(categories),
                "cooking_time": str(random.randint(10, 180)),
                "main_ingredient": random.choice(ingredients),
            }

            file.write(json.dumps(recipe, ensure_ascii=False) + "\n")

    print(f"Створено 200 000 записів: {path}")


if __name__ == "__main__":
    main()
