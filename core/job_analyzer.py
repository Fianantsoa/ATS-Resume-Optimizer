"""Job description keyword extraction."""

from __future__ import annotations

from collections import Counter

from config import DEFAULT_CONFIG
from utils.text_cleaner import clean_text, remove_stopwords, tokenize


def extract_keywords(job_description: str) -> list[str]:
    cleaned = clean_text(job_description)
    tokens = remove_stopwords(tokenize(cleaned))
    counts = Counter(tokens)
    if not counts:
        return []
    sorted_tokens = sorted(
        counts.items(), key=lambda item: (-item[1], item[0])
    )
    return [token for token, _ in sorted_tokens[: DEFAULT_CONFIG.max_keywords]]
