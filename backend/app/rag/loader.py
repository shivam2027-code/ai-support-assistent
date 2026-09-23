from pypdf import PdfReader


def load_pdf(file_path: str):

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "text": text,
                    "page": page_number
                }
            )

    return pages