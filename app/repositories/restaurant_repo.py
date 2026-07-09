from decimal import Decimal

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.restaurant import Restaurant


class RestaurantRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        stmt = select(Restaurant).where(Restaurant.id == restaurant_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 10) -> list[Restaurant]:
        stmt = select(Restaurant).limit(limit).order_by(Restaurant.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(
            self,
            name: str,
            city: str,
            address: str,
            description: str | None,
            average_check: int | None,
            rating: Decimal | None,
            latitude: Decimal | None,
            longitude: Decimal | None,
    ) -> Restaurant:

        restaurant = Restaurant(
            name=name,
            city=city,
            address=address,
            description=description,
            average_check=average_check,
            rating=rating,
            latitude=latitude,
            longitude=longitude
        )

        self.session.add(restaurant)
        await self.session.commit()
        await self.session.refresh(restaurant)
        return restaurant

    async def search_by_city(self, city: str, limit: int = 5) -> list[Restaurant]:

        stmt = ((select(Restaurant)
                .where(Restaurant.city.ilike(f"%{city}%"))
                .order_by(Restaurant.id))
                .limit(limit))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search(self, query: str, limit: int = 5) -> list[Restaurant]:

        stmt = (
            select(Restaurant)
            .where(
                or_(
                    Restaurant.name.ilike(f"%{query}%"),
                    Restaurant.city.ilike(f"%{query}%"),
                    Restaurant.address.ilike(f"%{query}%"),
                    Restaurant.description.ilike(f"%{query}%")
                )
            )
            .order_by(Restaurant.id)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
