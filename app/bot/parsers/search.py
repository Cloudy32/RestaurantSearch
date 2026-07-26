def parse_search_query(query_text: str) -> tuple[str, int | None]:

    query_text = query_text.strip()
    query_parts = query_text.split()

    max_average_check = None

    if not query_parts:
        return "", None
    elif query_parts[-1].isdigit():
        max_average_check = int(query_parts[-1])
        query = " ".join(query_parts[:-1])
    else:
        query = query_text

    return query, max_average_check
