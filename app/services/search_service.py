from app.db.models.restaurant import Restaurant

from app.repositories.restaurant_repo import RestaurantRepository


class SearchService:

    def __init__(self, repository: RestaurantRepository) -> None:
        self.repository = repository

    async def search_by_city(self, city: str) -> list[Restaurant]:
        return await self.repository.search_by_city(city)

    async def search(self, query: str) -> list[Restaurant]:
        return await self.repository.search(query)
