# utils.py
import hashlib
import re

def string_analysis(value: str) -> dict:
    value_cleaned = value.strip()
    sha256_hash = hashlib.sha256(value_cleaned.encode('utf-8')).hexdigest()

    # Case-insensitive palindrome check
    value_lower = value_cleaned.lower()
    is_palindrome = value_lower == value_lower[::-1]

    # Unique characters
    unique_characters = len(set(value_cleaned))

    # Word count (split by whitespace)
    word_count = len(value_cleaned.split())

    # Character frequency
    character_frequency_map = {}
    for char in value_cleaned:
        character_frequency_map[char] = character_frequency_map.get(char, 0) + 1

    return {
        "length": len(value_cleaned),
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency_map": character_frequency_map,
    }

# Basic natural language parser
def parse_natural_language_query(query: str) -> dict:
    query_lower = query.lower()
    filters = {}

    if "palindrome" in query_lower:
        filters["is_palindrome"] = True
    if "word count" in query_lower:
        # Example: "word count 3"
        match = re.search(r'word count (\d+)', query_lower)
        if match:
            filters["word_count"] = int(match.group(1))
    if "min length" in query_lower:
        match = re.search(r'min length (\d+)', query_lower)
        if match:
            filters["min_length"] = int(match.group(1))
    if "max length" in query_lower:
        match = re.search(r'max length (\d+)', query_lower)
        if match:
            filters["max_length"] = int(match.group(1))
    if "contains" in query_lower:
        match = re.search(r'contains (\w+)', query_lower)
        if match:
            filters["contains_character"] = match.group(1)

    return {"parsed_filters": filters, "original_query": query}
