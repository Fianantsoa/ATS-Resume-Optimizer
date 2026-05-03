"""Text normalization utilities."""

from __future__ import annotations

import re
from typing import Iterable

from config import DEFAULT_CONFIG

_TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9+#/-]*")


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_text(text: str) -> str:
    return normalize_whitespace(text.lower())


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN_PATTERN.findall(text)]


def remove_stopwords(tokens: Iterable[str]) -> list[str]:
    return [
        token
        for token in tokens
        if token not in DEFAULT_CONFIG.stopwords
        and len(token) >= DEFAULT_CONFIG.keyword_min_length
    ]
