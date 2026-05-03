"""Resume content analysis utilities."""

from __future__ import annotations

from collections import defaultdict

from config import DEFAULT_CONFIG
from utils.text_cleaner import remove_stopwords, tokenize


def analyze_cv(cv_text: str) -> dict:
    lines = [line.strip() for line in cv_text.splitlines() if line.strip()]
    sections = _extract_sections(lines)
    skills = _extract_skills(sections)
    experiences = sections.get("experience", [])
    return {
        "sections_present": sorted(sections.keys()),
        "skills": skills,
        "experience_lines": experiences,
        "sections": sections,
    }


def _extract_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = defaultdict(list)
    current_section = "summary"
    for line in lines:
        normalized = _normalize_heading(line)
        heading = _match_section_heading(normalized)
        if heading:
            current_section = heading
            continue
        sections[current_section].append(line)
    return dict(sections)


def _normalize_heading(text: str) -> str:
    return " ".join(text.lower().split())


def _match_section_heading(normalized_line: str) -> str | None:
    if not (
        DEFAULT_CONFIG.section_heading_min_length
        <= len(normalized_line)
        <= DEFAULT_CONFIG.section_heading_max_length
    ):
        return None
    for section, aliases in DEFAULT_CONFIG.section_aliases.items():
        if normalized_line in aliases:
            return section
    return None


def _extract_skills(sections: dict[str, list[str]]) -> list[str]:
    skill_lines = sections.get("skills", [])
    if not skill_lines:
        return []
    tokens = remove_stopwords(tokenize(" ".join(skill_lines)))
    return sorted(set(tokens))
