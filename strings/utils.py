from collections import Counter

def analyze_string(value: str):
    value_lower = value.lower()
    return {
        "length": len(value),
        "is_palindrome": value_lower == value_lower[::-1],
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "character_frequency_map": dict(Counter(value)),
    }

def parse_natural_language(query: str):
    filters = {}
    q = query.lower()
    if "palindrome" in q:
        filters["is_palindrome"] = True
    if "single word" in q:
        filters["word_count"] = 1
    if "letters" in q:
        import re
        m = re.search(r"(\d+)\s+letters", q)
        if m:
            filters["length"] = int(m.group(1))
    return filters
