from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Recipe:
    title: str
    category: str
    cooking_time: int | None
    main_ingredient: str

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")

        if not self.category.strip():
            raise ValueError("category must not be empty")

        if self.cooking_time is not None and (
            isinstance(self.cooking_time, bool) or self.cooking_time < 0
        ):
            raise ValueError("cooking_time must be non-negative")

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.category
