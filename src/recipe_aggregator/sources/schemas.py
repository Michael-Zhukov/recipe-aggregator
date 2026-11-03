from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..domain.models import Recipe
from ..domain.parsing import normalize_title, parse_cooking_time


class RecipeIn(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
    )

    title: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1)
    cooking_time: int | None = None
    main_ingredient: str = ""

    @field_validator("title", "category")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return normalize_title(value)

    @field_validator("cooking_time", mode="before")
    @classmethod
    def normalize_cooking_time(cls, value: object) -> int | None:
        return parse_cooking_time(value)

    @field_validator("main_ingredient", mode="before")
    @classmethod
    def normalize_ingredient(cls, value: object) -> object:
        if value is None:
            return ""
        return value

    def to_domain(self) -> Recipe:
        return Recipe(
            title=self.title,
            category=self.category,
            cooking_time=self.cooking_time,
            main_ingredient=self.main_ingredient,
        )
