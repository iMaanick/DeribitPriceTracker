from fastapi import APIRouter

from .index import index_router
from .prices import prices_router
root_router = APIRouter()

root_router.include_router(
    prices_router,
    prefix="/prices",
    tags=["prices"]
)
root_router.include_router(
    index_router,
)
