from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.cruds import dish_crud
from core.models import db_helper, Dish


async def get_dish_by_id(
    dish_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Dish:
    dish = await dish_crud.get_dish(session=session, dish_id=dish_id)
    if dish is not None:
        return dish
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Dish {dish_id} not found",
    )
