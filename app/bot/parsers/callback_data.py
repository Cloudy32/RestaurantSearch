def parse_restaurant_callback_data(
        data: str | None,
        expected_prefix: str,
) -> int | None:

    if data is None:
        return None

    parts = data.split(":")

    if len(parts) != 2:
        return None

    if parts[0] != expected_prefix:
        return None

    try:
        restaurant_id = int(parts[1])
        return restaurant_id
    except ValueError:
        return None
