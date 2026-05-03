import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.ats_service import ATSService  # noqa: E402


class TestScoring(unittest.TestCase):
    def test_full_score_with_complete_resume(self) -> None:
        service = ATSService()
        job_description = "Python SQL AWS"
        filler = " ".join(["python sql aws"] * 60)
        cv_text = "\n".join(
            [
                "Skills",
                f"- {filler}",
                "Experience",
                f"- {filler}",
                "Education",
                f"- {filler}",
            ]
        )

        result = service.analyze_text(cv_text, job_description)
        self.assertEqual(result.score, 100)

    def test_score_drops_when_sections_missing(self) -> None:
        service = ATSService()
        job_description = "Python SQL AWS"
        cv_text = "python sql aws " * 60

        result = service.analyze_text(cv_text, job_description)
        self.assertLess(result.score, 100)


if __name__ == "__main__":
    unittest.main()
