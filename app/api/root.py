from fastapi import APIRouter

from .index import index_router
from .users import users_router
from .prices import prices_router
root_router = APIRouter()
root_router.include_router(
    users_router,
    prefix="/users",
)
root_router.include_router(
    prices_router,
    prefix="/prices",
)
root_router.include_router(
    index_router,
)
