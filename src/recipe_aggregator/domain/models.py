from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Recipe:
    title: str
    category: str
    cooking_time: int | None
    main_ingredient: str

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.category
