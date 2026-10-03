from pypdf import PdfReader
from pathlib import Path
import re

def clean_extracted_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]

    text = "\n".join(lines)

    return text.strip()


def extract_text_from_pdf(filepath: str) -> str:
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    extracted_pages = []

    with file_path.open("rb") as file:
        reader = PdfReader(file)

        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if not page_text:
                continue

            clean_text = clean_extracted_text(page_text)

            if not clean_text:
                continue

            extracted_pages.append(
                {
                    "page_number": page_num,
                    "text": clean_text
                }
            )


        return extracted_pages