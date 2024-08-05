from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_application.core.models import Dish
from fastapi_application.core.schemas.dish import DishIn, DishUpdate


async def get_all_dishes(session: AsyncSession) -> list[Dish]:
    stmt = select(Dish).order_by(Dish.id)
    result: Result = await session.execute(stmt)
    dishes = result.scalars().all()
    return list(dishes)


async def create_dish(
    session: AsyncSession,
    dish_in: DishIn,
) -> Dish:
    dish = Dish(**dish_in.model_dump())
    try:
        session.add(dish)
        await session.commit()
        return dish
    except IntegrityError as e:
        if e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Такое блюдо уже существует",
            )


async def get_dish(
    session: AsyncSession,
    dish_id: int,
) -> Dish | None:
    return await session.get(Dish, dish_id)


async def update_dish(
    session: AsyncSession,
    dish_id: Dish,
    dish_update: DishUpdate,
) -> Dish:
    for name, value in dish_update.model_dump().items():
        setattr(dish_id, name, value)
    await session.commit()
    return dish_id


async def delete_dish(
    session: AsyncSession,
    dish_id: Dish,
) -> None:
    await session.delete(dish_id)
    await session.commit()
