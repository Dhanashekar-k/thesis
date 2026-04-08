"""
llm_client.py — LLM/VLM inference client for the AC model checker pipeline.

Provides a unified interface to call vLLM-hosted models (Qwen3 LLM and
Qwen3-VL VLM) via the OpenAI-compatible API.

Falls back to structured regex extraction when LLM/VLM is unavailable.
"""

from __future__ import annotations

import base64
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from config import LLMConfig


class InferenceClient:
    """
    Client for LLM/VLM inference via vLLM's OpenAI-compatible HTTP API.

    Usage:
        client = InferenceClient(config)
        result = client.complete("Extract guards from: ...")
        result = client.complete_with_image("Describe this diagram", "/path/to/img.jpg")
    """

    def __init__(self, config: LLMConfig):
        self.config = config

    def complete(
        self,
        prompt: str,
        system: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Send a text-only completion request."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        return self._chat(messages, temperature, max_tokens)

    def complete_with_image(
        self,
        prompt: str,
        image_path: str,
        system: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Send a multimodal (text + image) completion request."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        img_data = self._encode_image(image_path)
        if img_data is None:
            # Image not found — fall back to text only
            messages.append({"role": "user", "content": prompt})
        else:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": img_data}},
                    {"type": "text", "text": prompt},
                ],
            })

        return self._chat(messages, temperature, max_tokens)

    def complete_json(
        self,
        prompt: str,
        system: str = "",
        temperature: Optional[float] = None,
    ) -> dict:
        """Complete and parse JSON from the response."""
        raw = self.complete(prompt, system, temperature)
        return _extract_json(raw)

    def _chat(
        self,
        messages: list[dict],
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> str:
        payload = json.dumps({
            "model": self.config.model_name,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
        }).encode()

        url = f"{self.config.base_url}/chat/completions"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
            data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"]

    @staticmethod
    def _encode_image(path: str) -> Optional[str]:
        p = Path(path)
        if not p.exists():
            return None
        suffix = p.suffix.lower()
        mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".png": "image/png", ".webp": "image/webp"}.get(suffix, "image/jpeg")
        data = base64.b64encode(p.read_bytes()).decode()
        return f"data:{mime};base64,{data}"

    def close(self):
        pass


class MockInferenceClient:
    """
    Mock client for development/testing without a running LLM/VLM.
    Returns empty structured responses so the pipeline can run end-to-end.
    """

    def complete(self, prompt: str, **kwargs) -> str:
        return "{}"

    def complete_with_image(self, prompt: str, image_path: str, **kwargs) -> str:
        return "{}"

    def complete_json(self, prompt: str, **kwargs) -> dict:
        return {}

    def close(self):
        pass


def create_client(config: LLMConfig, enabled: bool = True) -> InferenceClient | MockInferenceClient:
    """Create an inference client, falling back to mock if disabled or unavailable."""
    if not enabled:
        return MockInferenceClient()
    try:
        # Quick health check
        req = urllib.request.Request(
            f"{config.base_url}/models",
            headers={"Authorization": f"Bearer {config.api_key}"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                return InferenceClient(config)
    except Exception:
        pass
    print(f"[llm_client] LLM at {config.base_url} unavailable, using mock client")
    return MockInferenceClient()


# ── JSON extraction helper ───────────────────────────────────────────────

def _extract_json(text: str) -> dict:
    """Extract a JSON object from LLM output that may contain markdown fences."""
    # Try raw parse first
    text = text.strip()
    # Remove thinking tags if Qwen3 thinking mode
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    # Remove markdown fences
    m = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find first { ... } block
        depth = 0
        start = -1
        for i, c in enumerate(text):
            if c == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0 and start >= 0:
                    try:
                        return json.loads(text[start:i+1])
                    except json.JSONDecodeError:
                        pass
        return {}
