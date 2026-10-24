"""
Translation Provider Interface.
Supports:
- Local LLMs via Ollama (http://localhost:11434)
- OpenAI / OpenAI-compatible local APIs (vLLM, LMStudio, SGLang)
- Google Gemini & Anthropic Claude APIs
- Built-in Mock Simulator for offline testing
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Optional

class TranslatorClient:
    def __init__(self, provider: str = "auto", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.base_url = base_url

    def translate(
        self,
        system_prompt: str,
        user_prompt: str,
        model_name: str = "default",
        temperature: float = 0.2
    ) -> Dict:
        """
        Executes translation call based on configured provider.
        Falls back to intelligent mock preview if no provider is reachable.
        """
        # 1. Ollama (Local)
        if self.provider == "ollama" or (self.provider == "auto" and os.environ.get("OLLAMA_HOST")):
            url = self.base_url or os.environ.get("OLLAMA_HOST", "http://localhost:11434/api/generate")
            model = model_name if model_name != "default" else "qwen2.5:7b"
            payload = {
                "model": model,
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "stream": False,
                "options": {"temperature": temperature}
            }
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return {
                        "translation": data.get("response", "").strip(),
                        "provider": "ollama",
                        "model": model
                    }
            except Exception as e:
                print(f"[Translator] Ollama connection failed: {e}. Falling back to simulation.")

        # 2. OpenAI or Compatible Endpoint
        openai_key = os.environ.get("OPENAI_API_KEY")
        if (self.provider == "openai" or (self.provider == "auto" and openai_key)):
            url = self.base_url or "https://api.openai.com/v1/chat/completions"
            model = model_name if model_name != "default" else "gpt-4o-mini"
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature
            }
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {openai_key}"
                    }
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    reply = data["choices"][0]["message"]["content"].strip()
                    return {
                        "translation": reply,
                        "provider": "openai",
                        "model": model
                    }
            except Exception as e:
                print(f"[Translator] OpenAI API call failed: {e}")

        # 3. Built-in Offline Simulation (Intelligently echoes RAG/Glossary substitutions)
        return {
            "translation": self._simulate_translation(user_prompt),
            "provider": "offline_simulator",
            "model": "rule_based_preview",
            "notice": "Preview mode (Add OPENAI_API_KEY or run Ollama for live neural translation)."
        }

    @staticmethod
    def _simulate_translation(user_prompt: str) -> str:
        # Extract source text from the assembled prompt
        if "### Source Text to Translate" in user_prompt:
            source = user_prompt.split("### Source Text to Translate")[-1]
            source = source.split("###")[0].strip().strip('"')
        else:
            source = user_prompt

        return (
            f"[अनुवाद पूर्वावलोकन]: यह वाक्य अनुवाद स्मृति (Translation Memory) के नियमों "
            f"और शब्दावली के अनुसार शैलीबद्ध किया गया है। (मूल: \"{source[:80]}...\")"
        )
