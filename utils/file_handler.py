"""File handling helpers."""

from __future__ import annotations

from pathlib import Path


class FileHandlingError(Exception):
    """Raised when file handling fails."""


def get_extension(filename: str) -> str:
    if not filename:
        raise FileHandlingError("Filename is required.")
    return Path(filename).suffix.lower().lstrip(".")


def read_bytes(uploaded_file) -> bytes:
    if uploaded_file is None:
        raise FileHandlingError("No file uploaded.")
    file_bytes = uploaded_file.read()
    if not file_bytes:
        raise FileHandlingError("Uploaded file is empty.")
    return file_bytes
