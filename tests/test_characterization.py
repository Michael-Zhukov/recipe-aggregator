from legacy.loader import process


def test_legacy_output_is_stable():
    recipes = process("data/recipes.json")

    assert len(recipes) == 10

    # Проверяем нормализацию названия
    assert recipes[0][0] == "борщ український"

    # Проверяем время приготовления
    assert recipes[0][2] == 90

    # Проверяем обработку нечислового значения
    assert recipes[7][2] == 0

    # Проверяем удаление дубликатов
    titles = [recipe[0] for recipe in recipes]
    assert titles.count("борщ український") == 1
