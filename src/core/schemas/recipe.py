from pydantic import BaseModel, ConfigDict


class BaseRecipe(BaseModel):
    dish_id: int
    name_recipe: str
    ingredients: str
    description: str


class RecipeIn(BaseRecipe):
    pass


class RecipeOut(BaseRecipe):
    id: int
    user_id: int
    count_views: int
    model_config = ConfigDict(from_attributes=True)


class RecipeUpdate(BaseRecipe):
    pass


class RecipeUpdatePartial(BaseRecipe):
    name_recipe: str | None = None
    ingredients: str | None = None
    description: str | None = None
