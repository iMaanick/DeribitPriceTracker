from .models import User
from .protocols.database import DatabaseGateway, UoW


async def new_user(
        database: DatabaseGateway,
        uow: UoW,
        name: str,
) -> int:
    user = User(name=name, id=1)
    await database.add_user(user)
    await uow.commit()
    return 1


