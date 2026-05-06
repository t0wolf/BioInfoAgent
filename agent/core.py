import json
import os
from typing import Any, Dict, List, Optional

try:
    import anthropic
    import httpx
except ImportError:
    anthropic = None
    httpx = None

try:
    import openai
except ImportError:
    openai = None

from .prompts import SYSTEM_PROMPT, INTERPRETATION_PROMPT
from .planner import PipelinePlanner


# MiMo endpoints: use OpenAI-compatible protocol (more reliable)
MIMO_ENDPOINTS = {
    "https://token-plan-cn.xiaomimimo.com/anthropic": "https://token-plan-cn.xiaomimimo.com/v1",
    "https://token-plan-sgp.xiaomimimo.com/anthropic": "https://token-plan-sgp.xiaomimimo.com/v1",
    "https://token-plan-ams.xiaomimimo.com/anthropic": "https://token-plan-ams.xiaomimimo.com/v1",
}


def _clear_proxy_env() -> Dict[str, str]:
    """Remove proxy env vars and return the saved values."""
    proxy_keys = [
        "ALL_PROXY", "all_proxy",
        "HTTP_PROXY", "http_proxy",
        "HTTPS_PROXY", "https_proxy",
    ]
    saved = {}
    for key in proxy_keys:
        if key in os.environ:
            saved[key] = os.environ.pop(key)
    return saved


def _restore_proxy_env(saved: Dict[str, str]):
    """Restore previously saved proxy env vars."""
    os.environ.update(saved)


class BioInfoAgent:
    """Core bioinformatics agent powered by Claude / MiMo API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.planner = PipelinePlanner()
        self.conversation_history: List[Dict] = []
        self.current_pipeline: Optional[Dict] = None
        self._client = None
        self._openai_client = None
        self._client_error: Optional[str] = None
        self._is_mimo = base_url is not None and "xiaomimimo.com" in (base_url or "")

    @property
    def client(self):
        """Lazy-initialize the API client."""
        if self._is_mimo:
            return self._get_openai_client()
        return self._get_anthropic_client()

    def _get_openai_client(self):
        """Get OpenAI-compatible client for MiMo."""
        if self._openai_client is None and self._client_error is None and self.api_key and openai:
            try:
                saved_env = _clear_proxy_env()
                # Convert Anthropic base URL to OpenAI-compatible
                oai_base = MIMO_ENDPOINTS.get(self.base_url, self.base_url)
                self._openai_client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=oai_base,
                )
                _restore_proxy_env(saved_env)
            except Exception as e:
                self._client_error = str(e)
        return self._openai_client

    def _get_anthropic_client(self):
        """Get Anthropic client."""
        if self._client is None and self._client_error is None and self.api_key and anthropic:
            try:
                saved_env = _clear_proxy_env()
                kwargs: Dict[str, Any] = {"api_key": self.api_key}
                if self.base_url:
                    kwargs["base_url"] = self.base_url
                self._client = anthropic.Anthropic(**kwargs)
                _restore_proxy_env(saved_env)
            except Exception as e:
                self._client_error = str(e)
        return self._client

    def _call_openai(self, system_prompt: str, messages: List[Dict], max_tokens: int = 4096) -> str:
        """Call MiMo via OpenAI-compatible API."""
        # Build messages with system prompt as first message
        oai_messages = [{"role": "system", "content": system_prompt}]
        oai_messages.extend(messages)
        response = self._openai_client.chat.completions.create(
            model=self.model,
            messages=oai_messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def _call_anthropic(self, system_prompt: str, messages: List[Dict], max_tokens: int = 4096) -> str:
        """Call via Anthropic Messages API."""
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text

    def _api_call(self, system_prompt: str, messages: List[Dict], max_tokens: int = 4096) -> str:
        """Unified API call - routes to OpenAI or Anthropic based on provider."""
        if not self.client:
            if self._client_error:
                return f"API connection error: {self._client_error}"
            return self._fallback_response("")

        try:
            if self._is_mimo:
                return self._call_openai(system_prompt, messages, max_tokens)
            else:
                return self._call_anthropic(system_prompt, messages, max_tokens)
        except Exception as e:
            return f"API error: {e}"

    def chat(self, user_message: str, context: Optional[Dict] = None) -> str:
        """Process a user message and return a response."""
        if not self.client:
            if self._client_error:
                return f"API connection error: {self._client_error}"
            return self._fallback_response(user_message)

        # Build messages from history
        messages = list(self.conversation_history)

        # Add context if provided
        if context:
            user_message = f"[Context: {json.dumps(context)}]\n\n{user_message}"

        messages.append({"role": "user", "content": user_message})

        try:
            assistant_message = self._api_call(SYSTEM_PROMPT, messages)

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message
        except Exception as e:
            return f"API error: {e}"

    def plan_pipeline(self, description: str) -> Dict[str, Any]:
        """Create a pipeline plan from a description."""
        pipeline = self.planner.plan_from_request(description)
        self.current_pipeline = pipeline
        return pipeline

    def get_pipeline_summary(self) -> str:
        """Get a summary of the current pipeline."""
        if not self.current_pipeline:
            return "No pipeline planned yet. Describe your analysis to get started."
        return self.planner.get_pipeline_summary(self.current_pipeline)

    def interpret_results(self, results: dict) -> str:
        """Interpret analysis results using the API."""
        if not self.client:
            return "API key not configured. Cannot interpret results."

        prompt = f"Please interpret these bioinformatics analysis results:\n\n{json.dumps(results, indent=2, default=str)}"

        try:
            return self._api_call(INTERPRETATION_PROMPT, [{"role": "user", "content": prompt}], max_tokens=2048)
        except Exception as e:
            return f"Interpretation error: {e}"

    def _fallback_response(self, message: str) -> str:
        """Provide basic responses without API access."""
        msg = message.lower()
        if any(kw in msg for kw in ["rna-seq", "rnaseq", "差异"]):
            pipeline = self.plan_pipeline(message)
            return self.planner.get_pipeline_summary(pipeline)
        elif any(kw in msg for kw in ["help", "帮助"]):
            return """I can help you with:
- **RNA-seq** analysis (QC -> alignment -> DE analysis)
- **ChIP-seq** peak calling
- **Variant calling** (WGS/WES)
- **Enrichment analysis** (GO/KEGG)
- **Sequence analysis** (BLAST, alignment)
- **Data format conversion**

Describe your analysis needs and I'll design a pipeline for you!"""
        else:
            return "Please provide your API key to enable the full AI agent, or describe your analysis type for pipeline planning."

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
