from pathlib import Path


def parse_txt(file_path: str) -> dict:
    path = Path(file_path)
    content = path.read_text(encoding="utf-8", errors="replace")
    return {"content": content, "pages": [{"page_number": 1, "text": content}]}
