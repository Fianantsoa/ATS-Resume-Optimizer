"""Resume parsing utilities."""

from __future__ import annotations

import fitz

from utils.file_handler import get_extension


class ParsingError(Exception):
    """Raised when parsing a resume fails."""


def parse_cv(file_bytes: bytes, filename: str) -> str:
    extension = get_extension(filename)
    if extension == "pdf":
        return _parse_pdf(file_bytes)
    if extension == "txt":
        return _parse_txt(file_bytes)
    raise ParsingError("Unsupported file type. Please upload a PDF or TXT file.")


def _parse_pdf(file_bytes: bytes) -> str:
    if not file_bytes:
        raise ParsingError("Uploaded PDF is empty.")
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as document:
            text = "\n".join(page.get_text() for page in document)
    except fitz.FileDataError as exc:
        raise ParsingError("Unable to read the PDF file.") from exc
    return text.strip()


def _parse_txt(file_bytes: bytes) -> str:
    if not file_bytes:
        raise ParsingError("Uploaded text file is empty.")
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return file_bytes.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    raise ParsingError("Unable to decode the text file.")
