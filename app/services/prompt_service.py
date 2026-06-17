from typing import List

PROMPT_TEMPLATE = """You are an AI assistant answering questions using uploaded documents.

Rules:
1. Only answer using supplied context.
2. Never hallucinate.
3. If answer not found say: \"The uploaded documents do not contain this information.\"
4. Cite source chunks whenever possible.

Context:
{context}

Question:
{question}

Answer:
"""

class PromptService:
    def build_context(self, chunks: List[dict], history: List[object]) -> str:
        history_text = ""
        if history:
            lines = []
            for message in history:
                lines.append(f"{message.role}: {message.content}")
            history_text = "\n".join(lines)
        chunk_text = "\n\n".join([
            f"Source {item['document_id']} page {item['page_number']}: {item['text']}"
            for item in chunks
        ])
        if history_text:
            return f"Conversation history:\n{history_text}\n\nRetrieved context:\n{chunk_text}"
        return f"Retrieved context:\n{chunk_text}"

    def build_prompt(self, context: str, question: str) -> str:
        return PROMPT_TEMPLATE.format(context=context, question=question)
