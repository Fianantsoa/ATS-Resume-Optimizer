"""Optimized resume generator."""

from __future__ import annotations

from config import DEFAULT_CONFIG
from core.optimizer import optimize_cv


def generate_optimized_cv(cv_text: str, missing_keywords: list[str]) -> str:
    optimized = optimize_cv(cv_text, missing_keywords)
    formatted_lines = _separate_section_headings(optimized.splitlines())
    return _collapse_blank_lines(formatted_lines)


def _separate_section_headings(lines: list[str]) -> list[str]:
    formatted: list[str] = []
    for line in lines:
        stripped = line.strip()
        if _is_section_heading(stripped) and formatted and formatted[-1].strip():
            formatted.append("")
        formatted.append(line.rstrip())
    return formatted


def _is_section_heading(line: str) -> bool:
    normalized = " ".join(line.lower().split())
    return any(
        normalized in aliases for aliases in DEFAULT_CONFIG.section_aliases.values()
    )


def _collapse_blank_lines(lines: list[str]) -> str:
    text = "\n".join(lines).strip()
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text
