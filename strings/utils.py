import hashlib
from collections import Counter
import re

def string_analysis(value: str):
    if not isinstance(value, str):
        raise TypeError("Value must be a string")

    # Clean for palindrome check — lowercase and remove spaces
    cleaned_value = re.sub(r"\s+", "", value.lower())

    # Compute SHA-256 hash (must match id exactly)
    sha256_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()

    # Build properties (case-insensitive palindrome)
    properties = {
        "length": len(value),
        "is_palindrome": cleaned_value == cleaned_value[::-1],
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": sha256_hash,
        "character_frequency_map": dict(Counter(value)),
    }

    return properties
