from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_application.core.models import Base
from fastapi_application.core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from fastapi_application.core.models import Recipe


class Dish(Base, IdIntPkMixin):
    __tablename__ = "dish"
    name_dish: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    recipe: Mapped[List["Recipe"]] = relationship(
        back_populates="dish", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Recipe(name={self.name_dish})>"
