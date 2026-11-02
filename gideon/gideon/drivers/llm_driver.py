"""
LLM Compute Driver for Gideon Agentic OS (NVIDIA NIM Hardware Layer).
"""

import httpx
from typing import Dict, Any, List, Optional
from gideon.drivers.base import BaseDriver

class LLMDriver(BaseDriver):
    def __init__(self, api_key: str, base_url: str, default_model: str):
        super().__init__("NVIDIA_NIM_COMPUTE_DRIVER")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self.chat_endpoint = f"{self.base_url}/chat/completions" if not self.base_url.endswith("/chat/completions") else self.base_url

    def initialize(self) -> bool:
        if not self.api_key:
            self.is_active = False
            return False
        self.is_active = True
        return True

    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        Executes a raw compute cycle (chat completion) on the neural hardware.
        """
        if not self.is_active:
            return {"ok": False, "error": "LLM Compute Driver is not initialized or missing API Key"}

        messages: List[Dict[str, str]] = kwargs.get("messages", [])
        model: str = kwargs.get("model") or self.default_model
        temperature: float = kwargs.get("temperature", 0.7)
        max_tokens: int = kwargs.get("max_tokens", 1024)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                res = client.post(self.chat_endpoint, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choice = data["choices"][0]
                    content = choice["message"]["content"]
                    usage = data.get("usage", {})
                    return {
                        "ok": True,
                        "content": content,
                        "model": model,
                        "tokens": usage.get("total_tokens", len(content.split()) * 2),
                        "raw": data
                    }
                else:
                    return {
                        "ok": False,
                        "error": f"NVIDIA NIM error {res.status_code}: {res.text}",
                        "status_code": res.status_code
                    }
        except Exception as exc:
            return {"ok": False, "error": f"Driver exception: {str(exc)}"}
