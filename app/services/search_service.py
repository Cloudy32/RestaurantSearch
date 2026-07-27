from decimal import Decimal

from app.db.models.restaurant import Restaurant

from app.repositories.restaurant_repo import RestaurantRepository


class SearchService:

    def __init__(self, repository: RestaurantRepository) -> None:
        self.repository = repository

    async def search(
            self,
            query: str,
            limit: int = 5,
            max_average_check: int | None = None,
            min_rating: Decimal | None = None
    ) -> list[Restaurant]:

        query = query.strip()

        if not query and max_average_check is None and min_rating is None:
            return []

        if query and len(query) < 2:
            return []

        return await self.repository.search(
            query=query,
            limit=limit,
            max_average_check=max_average_check,
            min_rating=min_rating
        )
