from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.cruds import recipe_crud
from api.api_v1.cruds.recipe_crud import (
    get_recipe,
    update_recipe,
    delete_client,
    get_all_recipes_by_dish,
)
from api.api_v1.fastapi_users import current_active_user, current_active_superuser
from core import settings
from core.models import db_helper, Recipe, User
from core.schemas.recipe import RecipeOut, RecipeIn, RecipeUpdate

from fastapi_cache.decorator import cache


router = APIRouter(
    prefix=settings.api.v1.recipes,
    tags=["Recipe"],
)


@router.post(
    "",
    response_model=RecipeOut,
    dependencies=[
        Depends(current_active_user),
    ],
)
async def create_new_recipe(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    recipe_in: RecipeIn,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Recipe:
    return await recipe_crud.create_recipe(
        session=session,
        recipe_in=recipe_in,
        user=user,
    )


@router.get(
    "/{recipe_id}",
    response_model=RecipeOut,
)
async def get_recipe_by_id(
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_recipe(
        session=session,
        recipe_id=recipe_id,
    )


@router.get(
    "/dish_name/{dish_name}",
    response_model=list[RecipeOut],
)
@cache(expire=30)
async def get_recipe_by_dish_name(
    dish_name: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_all_recipes_by_dish(
        session=session,
        dish_name=dish_name,
    )


@router.put(
    "/{recipe_id}",
    response_model=RecipeOut,
    dependencies=[
        Depends(current_active_user),
    ],
)
async def update_recipe_by_id(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    recipe_update: RecipeUpdate,
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    recipe = await session.get(Recipe, recipe_id)

    if recipe.user_id == user.id:
        return await update_recipe(
            session=session,
            recipe_update=recipe_update,
            recipe_id=recipe,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"You cannot change this recipe since you are not the creator of it.",
    )


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(current_active_user),
    ],
)
async def delete_recipe_by_id(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:

    recipe = await session.get(Recipe, recipe_id)

    if recipe.user_id == user.id:
        await delete_client(
            recipe_id=recipe,
            session=session,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You cannot remove this recipe since you are not the creator of it.",
        )
