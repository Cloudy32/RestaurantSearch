from decimal import Decimal

from app.bot.parsers.search import parse_search_query


def test_parse_search_query_without_average_check():
    query, max_average_check, min_rating = parse_search_query("Kizoku")

    assert query == "Kizoku"
    assert max_average_check is None
    assert min_rating is None

def test_parse_search_query_with_average_check():
    query, max_average_check, min_rating = parse_search_query("Kizoku 1500")

    assert query == "Kizoku"
    assert max_average_check == 1500
    assert min_rating is None

def test_parse_search_query_with_average_check_and_description():
    query, max_average_check, min_rating = parse_search_query("Koku Bryansk 1500")

    assert query == "Koku Bryansk"
    assert max_average_check == 1500
    assert min_rating is None

def test_parse_search_query_without_all():
    query, max_average_check, min_rating = parse_search_query(" ")

    assert query == ""
    assert max_average_check is None
    assert min_rating is None

def test_parse_search_query_only_with_check():
    query, max_average_check, min_rating = parse_search_query("1500")

    assert query == ""
    assert max_average_check == 1500
    assert min_rating is None

def test_parse_search_query_with_rating():
    query, max_average_check, min_rating = parse_search_query("1500 4.5")

    assert query == ""
    assert max_average_check == 1500
    assert min_rating == Decimal("4.5")
