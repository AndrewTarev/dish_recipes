from fastapi import APIRouter, Depends

from .dish_router import router as router_dish


router = APIRouter()

router.include_router(router_dish)
