from decimal import Decimal

from sqlalchemy import select, or_, nulls_last, and_
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

    async def search(
            self,
            query: str,
            limit: int = 5,
            max_average_check: int | None = None,
            min_rating: Decimal | None = None
    ) -> list[Restaurant]:

        search_words = query.split()
        search_conditions = []

        for word in search_words:
            search_conditions.append(
                or_(
                    Restaurant.name.ilike(f"%{word}%"),
                    Restaurant.city.ilike(f"%{word}%"),
                    Restaurant.address.ilike(f"%{word}%"),
                    Restaurant.description.ilike(f"%{word}%")
                )
            )

        stmt = (
            select(Restaurant)
            .where(and_(*search_conditions))
        )

        if max_average_check is not None:
            stmt = stmt.where(Restaurant.average_check <= max_average_check)

        if min_rating is not None:
            stmt = stmt.where(Restaurant.rating >= min_rating)

        stmt = stmt.order_by(
            nulls_last(Restaurant.rating.desc()),
            nulls_last(Restaurant.average_check.asc()),
            Restaurant.id.asc()
        )
        stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)
        return result.scalars().all()
