import httpx


class OverpassClient:

    def __init__(self) -> None:

        self.base_url = "https://overpass-api.de/api/interpreter"

    async def search_restaurants(self, city: str, limit: int = 10) -> dict:

        headers = {
            "User-Agent": "RestaurantSearchBot/0.1",
            "Accept": "application/json",
        }

        overpass_query = f"""
        [out:json][timeout:10];
        node["amenity"="restaurant"](53.15,34.20,53.35,34.55);
        out tags {limit};
        """

        data = {"data": overpass_query}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.base_url, params=data, headers=headers)
            response.raise_for_status()
            return response.json()

    def parse_restaurants(self, data: dict, city: str) -> list[dict]:

        restaurants = []
        elements = data.get("elements", [])

        for element in elements:

            tags = element.get("tags", {})
            name = tags.get("name")

            if not name:
                continue

            external_id = f"osm:{element.get('type')}:{element.get('id')}"

            restaurant = {
                "external_id": external_id,
                "name": name,
                "city": city,
                "address": tags.get("addr:full") or tags.get("addr:street"),
                "latitude": element.get("lat") or element.get("center", {}).get("lat"),
                "longitude": element.get("lon") or element.get("center", {}).get("lon"),
                "cuisine": tags.get("cuisine"),
            }

            restaurants.append(restaurant)

        return restaurants
