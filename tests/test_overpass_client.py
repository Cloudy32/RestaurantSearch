from app.integrations.overpass import OverpassClient

def test_parse_restaurants():
    client = OverpassClient()

    data = {
        "elements": [
            {
                "type": "node",
                "id": 123,
                "lat": 53.2,
                "lon": 34.3,
                "tags": {
                    "name": "Августин",
                    "amenity": "restaurant",
                    "cuisine": "german",
                    "addr:street": "Some street",
                },
            }
        ]
    }

    restaurants = client.parse_restaurants(data, city="Bryansk")

    assert len(restaurants) == 1
    assert restaurants[0]["external_id"] == "osm:node:123"
    assert restaurants[0]["name"] == "Августин"
    assert restaurants[0]["city"] == "Bryansk"
    assert restaurants[0]["address"] == "Some street"
    assert restaurants[0]["latitude"] == 53.2
    assert restaurants[0]["longitude"] == 34.3
    assert restaurants[0]["cuisine"] == "german"

