import fitz


def parse_pdf(file_path: str | bytes) -> dict:
    doc = fitz.open(file_path)
    pages = []
    content_parts = []
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text("text")
        pages.append({"page_number": page_number + 1, "text": text})
        content_parts.append(text)
    return {"content": "\n".join(content_parts), "pages": pages}
