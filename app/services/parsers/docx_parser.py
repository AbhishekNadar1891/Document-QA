from docx import Document as DocxDocument


def parse_docx(file_path: str) -> dict:
    doc = DocxDocument(file_path)
    paragraphs = []
    content_parts = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            paragraphs.append({"text": text})
            content_parts.append(text)
    return {"content": "\n".join(content_parts), "pages": paragraphs}
