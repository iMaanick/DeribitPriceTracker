from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.protocols.database import DatabaseGateway, UoW
from app.application.users import new_user
from .depends_stub import Stub

users_router = APIRouter()


@dataclass
class SomeResult:
    user_id: int


@users_router.get("/")
async def add_users(
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> SomeResult:
    user_id = await new_user(database, uow, "tishka17")
    user_id = 1
    return SomeResult(
        user_id=user_id,
    )


