from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.dish import DishOut, DishIn, DishUpdate
from api.api_v1.cruds import dish_crud
from api.api_v1.fastapi_users import current_active_superuser
from api.dependencies.dish_dependencies import get_dish_by_id
from core import settings
from core.models import Dish, db_helper

router = APIRouter(
    prefix=settings.api.v1.dishes,
    tags=["Dishes"],
)


@router.get(
    "",
    response_model=list[DishOut],
)
async def get_dishes(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> list[Dish]:
    return await dish_crud.get_all_dishes(session=session)


@router.post(
    "",
    response_model=DishOut,
    dependencies=[
        Depends(current_active_superuser),
    ],
)
async def create_dish(
    dish_in: DishIn,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Dish:
    return await dish_crud.create_dish(session=session, dish_in=dish_in)


@router.put(
    "/{dish_id}",
    response_model=DishOut,
    dependencies=[
        Depends(current_active_superuser),
    ],
)
async def update_dish(
    dish_update: DishUpdate,
    dish_id: Dish = Depends(get_dish_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await dish_crud.update_dish(
        session=session,
        dish_id=dish_id,
        dish_update=dish_update,
    )


@router.delete(
    "/{dish_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(current_active_superuser),
    ],
)
async def remove_dish(
    dish_id: Dish = Depends(get_dish_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await dish_crud.delete_dish(
        session=session,
        dish_id=dish_id,
    )
