import json
import random
from pathlib import Path


def main() -> None:
    random.seed(7)

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
    path.parent.mkdir(parents=True, exist_ok=True)

    previous = None

    with path.open("w", encoding="utf-8") as file:
        for i in range(200_000):
            if i % 10 == 3 and previous is not None:
                recipe = previous.copy()
            else:
                recipe = {
                    "title": f"Рецепт {i}",
                    "category": random.choice(categories),
                    "cooking_time": (str(random.randint(10, 180)) if i % 7 else "невідомо"),
                    "main_ingredient": random.choice(ingredients),
                }

            if i % 1000 == 0:
                recipe = dict(recipe, title="")

            file.write(json.dumps(recipe, ensure_ascii=False) + "\n")
            previous = recipe

    print(f"Створено 200 000 записів: {path}")


if __name__ == "__main__":
    main()
