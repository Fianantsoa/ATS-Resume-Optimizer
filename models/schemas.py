"""Data models for ATS Resume Optimizer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ATSResult:
    score: int
    missing_keywords: list[str]
    suggestions: list[str]
    optimized_cv: str

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "missing_keywords": self.missing_keywords,
            "suggestions": self.suggestions,
            "optimized_cv": self.optimized_cv,
        }
