from app.db.models.restaurant import Restaurant

from app.repositories.restaurant_repo import RestaurantRepository


class RestaurantService:

    def __init__(self, repository: RestaurantRepository) -> None:
        self.repository = repository

    async def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        return await self.repository.get_by_id(restaurant_id)


    async def get_all(self, limit: int = 5) -> list[Restaurant]:
        return await self.repository.get_all(limit)
