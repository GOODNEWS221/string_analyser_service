import hashlib
from collections import Counter
import re

def string_analysis(value: str):
    if not isinstance(value, str):
        raise TypeError("Value must be a string")
    
    cleaned_value = value.lower().replace(" ", "")
    sha256_hash = hashlib.sha256(value.encode()).hexdigest()
    properties = {
        "length": len(value),
        "is_palindrome": cleaned_value == cleaned_value[::-1],
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": sha256_hash,
        "character_frequency_map": dict(Counter(value)),
    }
    return properties


def parse_natural_language_query(query: str):
    if not query:
        raise ValueError("Query cannot be empty")

    query = query.lower()
    filters = {}

    if "palindromic" in query or "palindrome" in query:
        filters["is_palindrome"] = True
    if "single word" in query:
        filters["word_count"] = 1

    match = re.search(r"longer than (\d+)", query)
    if match:
        filters["min_length"] = int(match.group(1)) + 1

    match = re.search(r"shorter than (\d+)", query)
    if match:
        filters["max_length"] = int(match.group(1)) - 1

    match = re.search(r"contain(?:ing)? the letter (\w)", query)
    if match:
        filters["contains_character"] = match.group(1)

    if not filters:
        raise ValueError("Unable to parse natural language query")

    return {
        "original": query,
        "parsed_filters": filters
    }
