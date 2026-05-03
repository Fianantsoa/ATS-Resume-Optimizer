"""Resume optimization helpers."""

from __future__ import annotations

import re

from config import DEFAULT_CONFIG


def optimize_cv(cv_text: str, missing_keywords: list[str]) -> str:
    lines = _normalize_bullets(cv_text.splitlines())
    if not missing_keywords:
        return _finalize_text(lines)

    keywords_to_add = missing_keywords[: DEFAULT_CONFIG.max_injected_keywords]
    if not keywords_to_add:
        return _finalize_text(lines)

    insertion_line = f"Additional skills: {', '.join(keywords_to_add)}"
    updated_lines = _insert_into_skills_section(lines, insertion_line)
    return _finalize_text(updated_lines)


def _normalize_bullets(lines: list[str]) -> list[str]:
    normalized = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            normalized.append("")
            continue
        for prefix in DEFAULT_CONFIG.bullet_prefixes:
            if stripped.startswith(prefix):
                content = stripped[len(prefix) :].strip()
                normalized.append(f"- {content}" if content else "")
                break
        else:
            normalized.append(line.rstrip())
    return normalized


def _insert_into_skills_section(lines: list[str], insertion: str) -> list[str]:
    lower_lines = [line.strip().lower() for line in lines]
    skills_indices = [
        idx
        for idx, line in enumerate(lower_lines)
        if line in DEFAULT_CONFIG.section_aliases.get("skills", ())
    ]
    if skills_indices:
        insert_at = skills_indices[0] + 1
        return lines[:insert_at] + [insertion] + lines[insert_at:]
    return lines + ["", "Skills", insertion]


def _finalize_text(lines: list[str]) -> str:
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
