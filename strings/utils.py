import hashlib
import re

def string_analysis(value: str):
    """
    Analyze a string to calculate:
    - length
    - is_palindrome (case-insensitive)
    - unique_characters
    - word_count
    - sha256_hash
    - character_frequency_map
    """
    value_stripped = value.strip()
    length = len(value_stripped)
    # Case-insensitive palindrome check
    is_palindrome = value_stripped.lower() == value_stripped[::-1].lower()
    unique_characters = len(set(value_stripped))
    word_count = len(re.findall(r'\S+', value_stripped))
    sha256_hash = hashlib.sha256(value_stripped.encode('utf-8')).hexdigest()

    # Character frequency map
    char_freq = {}
    for c in value_stripped:
        char_freq[c] = char_freq.get(c, 0) + 1

    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency_map": char_freq
    }

def parse_natural_language_query(query: str):
    """
    Parse simple natural language queries to filters.
    Example queries:
      "all palindromes"
      "length >= 5"
      "strings containing 'a'"
    Returns a dictionary of filters:
    {
      "parsed_filters": {
          "is_palindrome": True,
          "min_length": 5,
          "contains_character": "a"
      }
    }
    """
    parsed = {"parsed_filters": {}}
    q = query.lower()

    if "palindrome" in q:
        parsed["parsed_filters"]["is_palindrome"] = True
    if "length >=" in q:
        match = re.search(r"length >= (\d+)", q)
        if match:
            parsed["parsed_filters"]["min_length"] = int(match.group(1))
    if "length <=" in q:
        match = re.search(r"length <= (\d+)", q)
        if match:
            parsed["parsed_filters"]["max_length"] = int(match.group(1))
    if "words" in q:
        match = re.search(r"words = (\d+)", q)
        if match:
            parsed["parsed_filters"]["word_count"] = int(match.group(1))
    if "contain" in q:
        match = re.search(r"contain(?:s)? '(\S)'", q)
        if match:
            parsed["parsed_filters"]["contains_character"] = match.group(1)

    return parsed
