from recipe_aggregator.services.pipeline import PipelineStats, parse_all


def test_pipeline_counts_invalid_records() -> None:
    rows: list[dict[str, object]] = [
        {
            "title": "Борщ",
            "category": "Супи",
            "cooking_time": 90,
        },
        {
            "title": "",
            "category": "Супи",
        },
        {
            "title": "Каша",
            "category": "",
        },
        {
            "title": "Салат",
            "category": "Салати",
            "cooking_time": "невідомо",
        },
    ]

    stats = PipelineStats()
    recipes = list(parse_all(rows, stats))

    assert stats.read == 4
    assert stats.invalid == 2
    assert len(recipes) == 2
    assert recipes[0].title == "борщ"
    assert recipes[1].cooking_time is None
