import httpx
import logging

from decimal import Decimal

from app.db.models.restaurant import Restaurant

from app.repositories.restaurant_repo import RestaurantRepository
from app.services.restaurant_service import RestaurantService
from app.integrations.overpass import OverpassClient

logger = logging.getLogger(__name__)


class SearchService:

    def __init__(
            self,
            repository: RestaurantRepository,
            restaurant_service: RestaurantService | None = None,
            overpass_client: OverpassClient | None = None,
    ) -> None:

        self.repository = repository
        self.restaurant_service = restaurant_service
        self.overpass_client = overpass_client

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

    async def search_with_external_fallback(self, query: str, limit: int = 5) -> list[Restaurant]:

        if not query:
            return []

        results = await self.search(query=query, limit=limit)
        if results:
            return results

        if self.restaurant_service is None or self.overpass_client is None:
            return []


        query = query.strip()
        words = query.split()

        if not words:
            return []

        city = words[-1]

        if len(words) > 1:
            name_query = words[:-1]
            name_query = " ".join(name_query)
        else:
            name_query = None

        try:
            data = await self.overpass_client.search_restaurants(city=city, limit=limit)
            restaurants = self.overpass_client.parse_restaurants(data=data, city=city)
        except httpx.HTTPError as ex:
            logger.warning(
                "Overpass search failed for city=%s: %s",
                city,
                ex,
            )
            return []

        if name_query:
            name_query = name_query.lower()
            rest = []

            for restaurant in restaurants:
                name = restaurant.get("name")

                if not name:
                    continue
                name = name.lower()

                if name_query in name:
                    rest.append(restaurant)

            results = await self.restaurant_service.get_or_create_from_external(rest)
            return results
        else:
            results = await self.restaurant_service.get_or_create_from_external(restaurants)

        return results




