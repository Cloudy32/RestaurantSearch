import httpx
import pytest

from app.services.search_service import SearchService


class FakeRepository:

    def __init__(self, result) -> None:
        self.result = result

    async def search(self, query, limit, max_average_check=None, min_rating=None):
        return self.result


class FakeOverpassClient:

    def __init__(self, parsed_restaurants=None, raise_error=False) -> None:
        self.raise_error = raise_error
        self.called = False
        self.parsed_restaurants = parsed_restaurants or []

    async def search_restaurants(self, city, limit):
        self.called = True
        if self.raise_error:
            raise httpx.HTTPError("Overpass failed")
        return {"elements": []}

    def parse_restaurants(self, data, city):
        return self.parsed_restaurants


class FakeRestaurantService:

    def __init__(self, result) -> None:
        self.result = result
        self.received_restaurants = None

    async def get_or_create_from_external(self, restaurants):
        self.received_restaurants = restaurants
        return self.result


@pytest.mark.asyncio
async def test_search_with_external_fallback_returns_db_results_without_overpass():
    db_restaurants = ["restaurant_from_db"]

    repository = FakeRepository(result=db_restaurants)
    overpass_client = FakeOverpassClient()

    service = SearchService(
        repository=repository,
        overpass_client=overpass_client,
        restaurant_service=None,
    )

    result = await service.search_with_external_fallback("Брянск")

    assert result == db_restaurants
    assert overpass_client.called is False


@pytest.mark.asyncio
async def test_search_with_external_fallback_returns_db_results_with_overpass():
    external_restaurants = [
        {
            "name": "Августин",
            "city": "Брянск",
            "source": "osm",
            "external_id": "node:123",
        }
    ]

    saved_restaurants = ["saved_restaurant"]

    repository = FakeRepository(result=[])
    overpass_client = FakeOverpassClient(parsed_restaurants=external_restaurants)
    restaurant_service = FakeRestaurantService(result=saved_restaurants)

    service = SearchService(
        repository=repository,
        overpass_client=overpass_client,
        restaurant_service=restaurant_service,
    )

    result = await service.search_with_external_fallback("Брянск")

    assert overpass_client.called is True
    assert restaurant_service.received_restaurants == external_restaurants
    assert result == saved_restaurants


@pytest.mark.asyncio
async def test_search_with_external_fallback_returns_empty_list_when_overpass_fail():

    repository = FakeRepository(result=[])
    overpass_client = FakeOverpassClient(parsed_restaurants=None, raise_error=True)
    restaurant_service = FakeRestaurantService(result=["should_not_return"])

    service = SearchService(
        repository=repository,
        overpass_client=overpass_client,
        restaurant_service=restaurant_service,
    )

    result = await service.search_with_external_fallback("Брянск")

    assert overpass_client.called is True
    assert restaurant_service.received_restaurants is None
    assert result == []


@pytest.mark.asyncio
async def test_search_with_external_fallback_filters_external_restaurants_by_name():

    external_restaurants = [
        {
            "name": "Августин",
            "city": "Брянск",
            "source": "osm",
            "external_id": "node:123",
        },
        {
            "name": "Шишка",
            "city": "Брянск",
            "source": "osm",
            "external_id": "node:2",
        },
    ]

    expected_restaurants = [
        {
            "name": "Августин",
            "city": "Брянск",
            "source": "osm",
            "external_id": "node:123",
        }
    ]

    saved_restaurants = ["saved_restaurant"]

    repository = FakeRepository(result=[])
    overpass_client = FakeOverpassClient(parsed_restaurants=external_restaurants)
    restaurant_service = FakeRestaurantService(result=saved_restaurants)

    service = SearchService(
        repository=repository,
        overpass_client=overpass_client,
        restaurant_service=restaurant_service,
    )

    result = await service.search_with_external_fallback("Августин Брянск")

    assert overpass_client.called is True
    assert restaurant_service.received_restaurants == expected_restaurants
    assert result == saved_restaurants

