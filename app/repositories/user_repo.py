from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_tg_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
            self,
            telegram_id: int,
            username: str | None,
            first_name: str | None
    ) -> User:

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user