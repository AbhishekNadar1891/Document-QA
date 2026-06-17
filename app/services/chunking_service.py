import re
import uuid
from typing import List

class ChunkingService:
    def _split_sentences(self, text: str) -> List[str]:
        pattern = r"(?<=[.!?])\s+"
        sentences = re.split(pattern, text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def chunk_text(self, document_id: str, text: str, pages: list, chunk_size: int = 700, chunk_overlap: int = 100) -> list:
        sentences = self._split_sentences(text)
        chunks = []
        current_chunk = []
        current_length = 0
        pointer = 0

        for sentence in sentences:
            sentence_length = len(sentence)
            if current_length + sentence_length > chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk).strip()
                chunks.append({
                    "document_id": document_id,
                    "chunk_id": str(uuid.uuid4()),
                    "page_number": self._page_number_for_pointer(pointer, pages),
                    "text": chunk_text,
                    "token_count": len(chunk_text.split()),
                })
                overlap_sentences = []
                while current_chunk and len(overlap_sentences) < chunk_overlap:
                    overlap_sentences.insert(0, current_chunk.pop())
                current_chunk = overlap_sentences
                current_length = sum(len(sentence) for sentence in current_chunk)
            current_chunk.append(sentence)
            current_length += sentence_length
            pointer += sentence_length

        if current_chunk:
            chunk_text = " ".join(current_chunk).strip()
            chunks.append({
                "document_id": document_id,
                "chunk_id": str(uuid.uuid4()),
                "page_number": self._page_number_for_pointer(pointer, pages),
                "text": chunk_text,
                "token_count": len(chunk_text.split()),
            })

        return chunks

    def _page_number_for_pointer(self, pointer: int, pages: list) -> int | None:
        if not pages:
            return None
        accumulated = 0
        for page in pages:
            text = page.get("text", "")
            accumulated += len(text)
            if pointer <= accumulated:
                return page.get("page_number")
        return pages[-1].get("page_number")
