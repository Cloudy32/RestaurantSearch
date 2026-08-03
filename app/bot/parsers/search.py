from decimal import Decimal, InvalidOperation


def parse_search_query(query_text: str) -> tuple[str, int | None, Decimal | None]:

    query_text = query_text.strip()
    query_parts = query_text.split()

    max_average_check = None
    min_rating = None

    if not query_parts:
        return "", None, None

    last_part = query_parts[-1]

    try:
        rating_candidate = Decimal(last_part)
    except InvalidOperation:
        rating_candidate = None

    if rating_candidate is not None and 0 <= rating_candidate <= 5:
        min_rating = rating_candidate
        query_parts = query_parts[:-1]

    if query_parts and query_parts[-1].isdigit():
        check_candidate = query_parts[-1]
        if check_candidate.isdigit() and int(check_candidate) > 5:
            max_average_check = int(check_candidate)
            query_parts = query_parts[:-1]

    query = " ".join(query_parts)

    return query, max_average_check, min_rating
