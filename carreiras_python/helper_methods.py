def normalize_searched_terms(searched_terms):
    words = searched_terms.split(" ")
    filtered = []  # words with more than 2 letters
    for word in words:  # to remove words with less than 3 words
        if len(word) >= 3:
            filtered.append(word)
    if len(filtered) == 0:
        return False
    string_query = f"SELECT * FROM jobs WHERE "
    for i, word in enumerate(filtered, start=1):
        if len(filtered) == 1:
            string_query = string_query + f"title LIKE '%{word}%'"
            return string_query
        if len(filtered) > 1 and i < len(filtered):
            string_query = string_query + f"title LIKE '%{word}%'" + " OR "
        if 1 < len(filtered) == i:
            string_query = string_query + f"title LIKE '%{word}%'"
            return string_query