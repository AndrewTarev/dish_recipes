from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Recipe, User
from core.schemas.recipe import RecipeIn, RecipeUpdate, RecipeUpdatePartial


async def create_recipe(
    session: AsyncSession,
    recipe_in: RecipeIn,
    user: User,
) -> Recipe:
    recipe = Recipe(**recipe_in.model_dump())
    session.add(recipe)
    recipe.user_id = user.id
    await session.commit()
    return recipe


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

    recipe = await session.get(Recipe, recipe_id)
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
