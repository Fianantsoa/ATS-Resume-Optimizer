import unittest

from services.ats_service import ATSService


class TestScoring(unittest.TestCase):
    def test_total_score_full_match(self) -> None:
        service = ATSService()
        score = service._compute_total_score(1.0, 1.0, 1.0, 1.0)
        self.assertEqual(score, 100)

    def test_total_score_zero_match(self) -> None:
        service = ATSService()
        score = service._compute_total_score(0.0, 0.0, 0.0, 0.0)
        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
