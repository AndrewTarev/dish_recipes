import asyncio

from fastapi import HTTPException, status
from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Recipe, User, Dish, db_helper
from core.schemas.recipe import RecipeIn, RecipeUpdate, RecipeUpdatePartial


async def create_recipe(
    session: AsyncSession,
    recipe_in: RecipeIn,
    user: User,
) -> Recipe:
    try:
        recipe: Recipe = Recipe(**recipe_in.model_dump())
        session.add(recipe)
        recipe.user_id = user.id
        await session.commit()
        return recipe
    except IntegrityError as e:
        if e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категория такого блюда не существует {recipe.dish_id}",
            )


async def get_all_recipes_by_dish(
    dish_name: str,
    session: AsyncSession,
) -> list[Recipe]:
    stmt = (
        select(Recipe)
        .join(Dish, Dish.id == Recipe.dish_id)
        .where(Dish.name_dish == dish_name)
    )
    res = await session.execute(stmt)
    recipes = res.scalars().all()

    return list(recipes)


async def get_recipe(
    recipe_id: int,
    session: AsyncSession,
) -> Recipe | None:

    stmt = (
        update(Recipe)
        .where(Recipe.id == recipe_id)
        .values(count_views=Recipe.count_views + 1)
    )
    await session.execute(stmt)

    recipe: Recipe | None = await session.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id={recipe_id} not found",
        )
    await session.commit()
    return recipe


async def update_recipe(
    session: AsyncSession,
    recipe_id: Recipe,
    recipe_update: RecipeUpdate | RecipeUpdatePartial,
    partial: bool = False,
) -> Recipe:
    for name, value in recipe_update.model_dump(exclude_unset=partial).items():
        setattr(recipe_id, name, value)
    await session.commit()
    return recipe_id


async def delete_client(
    session: AsyncSession,
    recipe_id: int,
) -> None:
    await session.delete(recipe_id)
    await session.commit()


async def main():
    async with db_helper.session_factory() as session:
        await get_all_recipes_by_dish(session=session, dish_name="Пюре")


if __name__ == "__main__":
    asyncio.run(main())
