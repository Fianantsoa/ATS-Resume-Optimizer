import sys
import unittest
from pathlib import Path

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.parser import parse_cv  # noqa: E402


class TestParser(unittest.TestCase):
    def test_parse_txt(self) -> None:
        content = b"Sample Resume Text"
        result = parse_cv(content, "resume.txt")
        self.assertEqual(result, "Sample Resume Text")

    def test_parse_pdf(self) -> None:
        document = fitz.open()
        page = document.new_page()
        page.insert_text((72, 72), "PDF Resume")
        pdf_bytes = document.tobytes()
        document.close()

        result = parse_cv(pdf_bytes, "resume.pdf")
        self.assertIn("PDF Resume", result)


if __name__ == "__main__":
    unittest.main()
