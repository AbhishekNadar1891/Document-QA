import logging
import os
import requests
from typing import Generator
from app.config.settings import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.openrouter_api_key = settings.OPENROUTER_API_KEY
        self.provider = self._resolve_provider()

    def _resolve_provider(self) -> str:
        if self.openrouter_api_key:
            return "openrouter"
        if self.openai_api_key:
            return "openai"
        raise RuntimeError("No LLM provider configured")

    def generate(self, prompt: str) -> str:
        if self.provider == "openrouter":
            return self._generate_openrouter(prompt)
        return self._generate_openai(prompt)

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        if self.provider == "openrouter":
            yield from self._stream_openrouter(prompt)
        else:
            yield from self._stream_openai(prompt)

    def _generate_openai(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=self.openai_api_key)
        response = client.responses.create(
            model=settings.LLM_MODEL,
            input=prompt,
        )
        if response.output:
            return "".join([segment["content"] for segment in response.output if segment.get("type") == "output_text"])
        return ""

    def _stream_openai(self, prompt: str):
        from openai import OpenAI
        client = OpenAI(api_key=self.openai_api_key)
        stream = client.responses.stream(
            model=settings.LLM_MODEL,
            input=prompt,
        )
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

    def _generate_openrouter(self, prompt: str) -> str:
        url = "https://openrouter.ai/v1/chat/completions"
        payload = {
            "model": settings.LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _stream_openrouter(self, prompt: str):
        url = "https://openrouter.ai/v1/chat/completions"
        payload = {
            "model": settings.LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        with requests.post(url, json=payload, headers=headers, stream=True, timeout=60) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data:"):
                    continue
                payload = line[len("data:"):].strip()
                if payload == "[DONE]":
                    break
                yield payload
