import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.ats_service import ATSService  # noqa: E402


class TestOptimizer(unittest.TestCase):
    def test_optimized_cv_includes_missing_keywords(self) -> None:
        service = ATSService()
        job_description = "Python AWS"
        cv_text = "\n".join(
            [
                "Skills",
                "- python",
                "Experience",
                "- Built analytics pipelines.",
                "Education",
                "- Bachelor of Science",
            ]
        )

        result = service.analyze_text(cv_text, job_description)

        self.assertIn("aws", result.missing_keywords)
        self.assertIn("additional skills: aws", result.optimized_cv.lower())


if __name__ == "__main__":
    unittest.main()
