from fastapi import APIRouter, Depends

from .dish_router import router as router_dish
from .recipe_router import router as router_recipe


router = APIRouter()

router.include_router(router_dish)
router.include_router(router_recipe)
