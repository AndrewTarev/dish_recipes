from pydantic import BaseModel, ConfigDict


class BaseDish(BaseModel):
    name_dish: str


class DishIn(BaseDish):
    pass


class DishOut(BaseDish):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DishUpdate(BaseDish):
    pass
