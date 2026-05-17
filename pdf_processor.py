"""
PDF processing module.
Handles reading and extracting text from PDF files.
"""

import PyPDF2
from pathlib import Path


def read_pdf(pdf_path: str) -> str:
    """
    Read and extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text from all pages

    Raises:
        FileNotFoundError: If the PDF file is not found
        PyPDF2.PdfReadError: If the PDF cannot be read
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    study_material = ""

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            study_material += page.extract_text()

    return study_material
