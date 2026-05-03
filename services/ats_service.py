"""Service layer orchestrating ATS analysis."""

from __future__ import annotations

from config import DEFAULT_CONFIG, ATSConfig
from core.cv_analyzer import analyze_cv
from core.generator import generate_optimized_cv
from core.job_analyzer import extract_keywords
from core.matcher import match_keywords
from core.parser import parse_cv
from models.schemas import ATSResult
from utils.file_handler import read_bytes
from utils.text_cleaner import clean_text


class ATSService:
    """Main service for ATS resume analysis."""

    def __init__(self, config: ATSConfig | None = None) -> None:
        self.config = config or DEFAULT_CONFIG

    def analyze_file(
        self, file_bytes: bytes, filename: str, job_description: str
    ) -> ATSResult:
        cv_text = parse_cv(file_bytes, filename)
        return self.analyze_text(cv_text, job_description)

    def analyze_upload(self, uploaded_file, job_description: str) -> ATSResult:
        file_bytes = read_bytes(uploaded_file)
        filename = getattr(uploaded_file, "name", "")
        if not filename:
            raise ValueError("Uploaded file must have a name.")
        return self.analyze_file(file_bytes, filename, job_description)

    def analyze_text(self, cv_text: str, job_description: str) -> ATSResult:
        job_keywords = extract_keywords(job_description)
        cv_analysis = analyze_cv(cv_text)
        match_data = match_keywords(job_keywords, cv_text)

        section_score = self._compute_section_score(cv_analysis["sections_present"])
        density_score = self._compute_density_score(match_data["keyword_density"])
        formatting_score = self._compute_formatting_score(cv_text, cv_analysis)
        total_score = self._compute_total_score(
            match_data["match_ratio"],
            section_score,
            density_score,
            formatting_score,
        )

        suggestions = self._build_suggestions(
            cv_analysis,
            match_data,
            density_score,
            formatting_score,
        )
        optimized_cv = generate_optimized_cv(cv_text, match_data["missing"])
        return ATSResult(
            score=total_score,
            missing_keywords=match_data["missing"],
            suggestions=suggestions,
            optimized_cv=optimized_cv,
        )

    def _compute_section_score(self, sections_present: list[str]) -> float:
        required = set(self.config.required_sections)
        if not required:
            return 0.0
        present = required.intersection(sections_present)
        return len(present) / len(required)

    def _compute_density_score(self, density: float) -> float:
        target = self.config.keyword_density_target
        if target <= 0:
            return 0.0
        return min(density / target, 1.0)

    def _compute_formatting_score(self, cv_text: str, cv_analysis: dict) -> float:
        checks = [
            self._has_bullets(cv_text),
            self._has_section_headings(cv_analysis),
            self._has_minimum_length(cv_text),
        ]
        return sum(checks) / len(checks) if checks else 0.0

    def _has_bullets(self, cv_text: str) -> bool:
        for line in cv_text.splitlines():
            stripped = line.strip()
            if any(stripped.startswith(prefix) for prefix in self.config.bullet_prefixes):
                return True
        return False

    def _has_section_headings(self, cv_analysis: dict) -> bool:
        return len(cv_analysis.get("sections_present", [])) > 1

    def _has_minimum_length(self, cv_text: str) -> bool:
        return len(clean_text(cv_text).split()) >= self.config.formatting_min_word_count

    def _compute_total_score(
        self,
        match_ratio: float,
        section_score: float,
        density_score: float,
        formatting_score: float,
    ) -> int:
        weights = self.config.ats_score_weights
        total = (
            match_ratio * weights["keyword_match"]
            + section_score * weights["sections"]
            + density_score * weights["density"]
            + formatting_score * weights["formatting"]
        )
        return int(round(total * 100))

    def _build_suggestions(
        self,
        cv_analysis: dict,
        match_data: dict,
        density_score: float,
        formatting_score: float,
    ) -> list[str]:
        suggestions: list[str] = []
        if match_data["missing"]:
            suggestions.append(
                "Add relevant keywords from the job description to boost ATS match."
            )
        missing_sections = set(self.config.required_sections) - set(
            cv_analysis.get("sections_present", [])
        )
        if missing_sections:
            suggestions.append(
                "Include these core sections to improve structure: "
                + ", ".join(sorted(missing_sections))
                + "."
            )
        if density_score < 0.7:
            suggestions.append(
                "Increase keyword usage throughout your CV to improve keyword density."
            )
        if formatting_score < 1:
            suggestions.append(
                "Use clear headings and bullet points for readability."
            )
        if not suggestions:
            suggestions.append("Your resume aligns well with the job description.")
        return suggestions
