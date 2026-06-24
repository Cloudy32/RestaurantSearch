from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.favorite import Favorite


class FavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_user_and_restaurant(
            self,
            user_id: int,
            restaurant_id: int
    ) -> Favorite | None:

        stmt = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.restaurant_id == restaurant_id,
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create_favorite(self, user_id: int, restaurant_id: int) -> Favorite:

        favorite = Favorite(
            user_id=user_id,
            restaurant_id=restaurant_id,
        )

        self.session.add(favorite)
        await self.session.commit()
        await self.session.refresh(favorite)

        return favorite

    async def get_all_favorites(self, user_id: int) -> list[Favorite]:

        stmt = select(Favorite).options(selectinload(Favorite.restaurant)).where(Favorite.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_favorite(self, favorite: Favorite) -> None:

        await self.session.delete(favorite)
        await self.session.commit()