from typing import TYPE_CHECKING, List

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.models import Base
from core.models.mixins.id_int_pk import IdIntPkMixin
from core.models.recipe import Recipe
from core.models.types.user_id import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    __tablename__ = "user"
    nickname: Mapped[str] = mapped_column(String(30), unique=True, nullable=True)

    recipe: Mapped[List["Recipe"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
