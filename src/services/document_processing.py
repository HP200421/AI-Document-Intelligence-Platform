from pypdf import PdfReader
from pathlib import Path
import re

def clean_extracted_text(text: str) -> str:
    # Normalize Windows/Mac line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing/leading whitespace from each line
    lines = [line.strip() for line in text.split("\n")]

    # Remove empty lines
    lines = [line for line in lines if line]

    # Collapse excessive spaces/tabs
    text = "\n".join(lines)
    text = re.sub(r"[ \t]+", " ", text)

    # Avoid excessive consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(filepath: str) -> str:
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    extracted_pages: list[str] = []

    with file_path.open("rb") as file:
        reader = PdfReader(file)

        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if page_text:
                extracted_pages.append(
                    f"--- Page {page_num} ---\n"
                    f"{page_text.strip()}\n"
                )


    extracted_text = "\n\n".join(extracted_pages)

    return clean_extracted_text(extracted_text)


    
