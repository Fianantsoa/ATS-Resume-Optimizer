import unittest

from core.matcher import match_keywords


class TestMatcher(unittest.TestCase):
    def test_match_keywords(self) -> None:
        job_keywords = ["python", "sql", "aws"]
        cv_text = "Experienced in Python and SQL."
        result = match_keywords(job_keywords, cv_text)

        self.assertEqual(set(result["matched"]), {"python", "sql"})
        self.assertEqual(result["missing"], ["aws"])
        self.assertAlmostEqual(result["match_ratio"], 2 / 3)


if __name__ == "__main__":
    unittest.main()
