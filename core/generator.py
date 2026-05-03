"""Optimized resume generator."""

from __future__ import annotations

from core.optimizer import optimize_cv


def generate_optimized_cv(cv_text: str, missing_keywords: list[str]) -> str:
    return optimize_cv(cv_text, missing_keywords)
