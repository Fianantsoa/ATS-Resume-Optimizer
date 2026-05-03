"""Keyword matching utilities."""

from __future__ import annotations

from collections import Counter

from utils.text_cleaner import clean_text, tokenize


def match_keywords(job_keywords: list[str], cv_text: str) -> dict:
    cleaned_cv = clean_text(cv_text)
    tokens = tokenize(cleaned_cv)
    token_counts = Counter(tokens)
    job_keywords_unique = list(dict.fromkeys(job_keywords))
    matched = [keyword for keyword in job_keywords_unique if keyword in token_counts]
    missing = [keyword for keyword in job_keywords_unique if keyword not in token_counts]
    total_keywords = len(job_keywords_unique)
    match_ratio = len(matched) / total_keywords if total_keywords else 0.0
    total_tokens = sum(token_counts.values())
    density = (
        sum(token_counts[keyword] for keyword in matched) / total_tokens
        if total_tokens
        else 0.0
    )
    return {
        "matched": matched,
        "missing": missing,
        "match_ratio": match_ratio,
        "keyword_density": density,
    }
