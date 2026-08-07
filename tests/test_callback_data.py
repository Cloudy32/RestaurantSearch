from app.bot.parsers.callback_data import parse_restaurant_callback_data


def test_parse_restaurant_callback_data_with_valid_add_favorite():
    restaurant_id = parse_restaurant_callback_data(
        "add_favorite:123",
        "add_favorite",
    )

    assert restaurant_id == 123


def test_parse_restaurant_callback_data_with_valid_remove_favorite():
    restaurant_id = parse_restaurant_callback_data(
        "remove_favorite:123",
        "remove_favorite",
    )

    assert restaurant_id == 123


def test_parse_restaurant_callback_data_with_none():
    restaurant_id = parse_restaurant_callback_data(
        None,
        "add_favorite",
    )

    assert restaurant_id is None


def test_parse_restaurant_callback_data_with_wrong_prefix():
    restaurant_id = parse_restaurant_callback_data(
        "remove_favorite:123",
        "add_favorite",
    )

    assert restaurant_id is None


def test_parse_restaurant_callback_data_with_invalid_id():
    restaurant_id = parse_restaurant_callback_data(
        "add_favorite:abc",
        "add_favorite",
    )

    assert restaurant_id is None


def test_parse_restaurant_callback_data_with_invalid_format():
    restaurant_id = parse_restaurant_callback_data(
        "add_favorite",
        "add_favorite",
    )

    assert restaurant_id is None

