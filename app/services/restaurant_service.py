from app.db.models.restaurant import Restaurant

from app.repositories.restaurant_repo import RestaurantRepository


class RestaurantService:

    def __init__(self, repository: RestaurantRepository) -> None:
        self.repository = repository

    async def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        return await self.repository.get_by_id(restaurant_id)


    async def get_all(self, limit: int = 5) -> list[Restaurant]:
        return await self.repository.get_all(limit)

    async def get_by_source_and_external_id(
            self,
            source: str,
            external_id: str
    ) -> Restaurant | None:

        return await self.repository.get_by_source_and_external_id(source, external_id)

    async def get_or_create_from_external(self, restaurants: list[dict]) -> list[Restaurant]:

        created_or_existing_restaurants = []

        for restaurant in restaurants:

            source = restaurant.get("source")
            external_id = restaurant.get("external_id")
            name = restaurant.get("name")
            city = restaurant.get("city")
            address = restaurant.get("address")
            description = restaurant.get("cuisine")
            longitude = restaurant.get("longitude")
            latitude = restaurant.get("latitude")

            if not source or not external_id or not name or not city:
                continue

            existing = await self.repository.get_by_source_and_external_id(source, external_id)

            if existing:
                created_or_existing_restaurants.append(existing)
                continue

            created = await self.repository.create(
                name=name,
                city=city,
                description=description,
                address=address or "Не указан",
                average_check=None,
                rating=None,
                longitude=longitude,
                latitude=latitude,
                source=source,
                external_id=external_id,
            )

            created_or_existing_restaurants.append(created)

        return created_or_existing_restaurants
