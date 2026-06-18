import asyncio
from decimal import Decimal

from app.db.session import async_session_maker, engine
from app.repositories.restaurant_repo import RestaurantRepository

async def main() -> None:
    async with async_session_maker() as session:
        repository = RestaurantRepository(session)

        await repository.create(
            name="Kizoku",
            city="Bryansk",
            address="Voistrochenko 5",
            description="Koku",
            average_check=1500,
            rating=Decimal("5"),
            latitude=Decimal("47.2151"),
            longitude=Decimal("-122.4475"),
        )

        await repository.create(
            name="Aristo",
            city="Bryansk",
            address="gorbatogo 20",
            description="pepe",
            average_check=1000,
            rating=Decimal("5"),
            latitude=Decimal("33.2161"),
            longitude=Decimal("122.4475"),
        )

        await repository.create(
            name="White Rabbyt",
            city="Moscow",
            address="Red Square",
            description="fafa",
            average_check=None,
            rating=None,
            latitude=None,
            longitude=None,
        )

        await repository.create(
            name="Puska",
            city="Kaluga",
            address="Velikogo Egora 7a",
            description="pupaZalupa",
            average_check=99999,
            rating=Decimal("1"),
            latitude=Decimal("47.2111"),
            longitude=Decimal("-12.4475"),
        )


    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())