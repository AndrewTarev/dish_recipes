from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from core.models import Dish, User


class Recipe(Base, IdIntPkMixin):
    __tablename__ = "recipe"

    dish_id: Mapped[int] = mapped_column(
        ForeignKey("dish.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    name_recipe: Mapped[str] = mapped_column(String(264), nullable=False)
    count_views: Mapped[int] = mapped_column(default=0)
    ingredients: Mapped[str] = mapped_column(String(264), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    dish: Mapped["Dish"] = relationship(back_populates="recipe", single_parent=True)
    user: Mapped["User"] = relationship(back_populates="recipe", single_parent=True)

    def __repr__(self):
        return f"<Recipe(name_recipe={self.name_recipe})>"
