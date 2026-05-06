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

# ──────────────────────────────────────────────────────────────
# Provider Registry
# Each provider has: protocol, base_url, models
# Protocol "anthropic" uses Anthropic SDK
# Protocol "openai" uses OpenAI SDK (compatible with most providers)
# ──────────────────────────────────────────────────────────────

PROVIDERS: Dict[str, Dict[str, Any]] = {
    "anthropic": {
        "name": "Anthropic",
        "protocol": "anthropic",
        "base_url": None,
        "models": [
            "claude-opus-4-7",
            "claude-opus-4-6",
            "claude-sonnet-4-6",
            "claude-haiku-4-5-20251001",
        ],
    },
    "openai": {
        "name": "OpenAI",
        "protocol": "openai",
        "base_url": "https://api.openai.com/v1",
        "models": [
            "gpt-5.5-high",
            "gpt-5.4-high",
            "gpt-5.2-chat-latest",
            "gpt-4o",
            "gpt-4o-mini",
        ],
    },
    "gemini": {
        "name": "Google Gemini",
        "protocol": "openai",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "models": [
            "gemini-3.1-pro-preview",
            "gemini-3-pro",
            "gemini-3-flash",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
        ],
    },
    "xai": {
        "name": "xAI Grok",
        "protocol": "openai",
        "base_url": "https://api.x.ai/v1",
        "models": [
            "grok-4.20-beta",
            "grok-4.1-thinking",
            "grok-3",
            "grok-3-mini",
        ],
    },
    "deepseek": {
        "name": "DeepSeek",
        "protocol": "openai",
        "base_url": "https://api.deepseek.com/v1",
        "models": [
            "deepseek-v4-pro",
            "deepseek-r1",
            "deepseek-chat",
            "deepseek-reasoner",
        ],
    },
    "mimo": {
        "name": "Xiaomi MiMo",
        "protocol": "openai",
        "base_url": "https://token-plan-cn.xiaomimimo.com/v1",
        "models": [
            "mimo-v2.5-pro",
            "MiMo-7B",
        ],
    },
    "custom": {
        "name": "Custom",
        "protocol": "openai",
        "base_url": None,
        "models": [],
    },
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
    """Core bioinformatics agent powered by multiple AI providers."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-opus-4-7",
        base_url: Optional[str] = None,
        provider: str = "anthropic",
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.provider = provider
        self.planner = PipelinePlanner()
        self.conversation_history: List[Dict] = []
        self.current_pipeline: Optional[Dict] = None
        self._client = None
        self._client_error: Optional[str] = None

        # Resolve provider config
        prov = PROVIDERS.get(provider, PROVIDERS["anthropic"])
        self._protocol = prov["protocol"]
        # Use provider's base_url if user didn't specify one
        if self.base_url is None and prov.get("base_url"):
            self.base_url = prov["base_url"]

    @property
    def client(self):
        """Lazy-initialize the API client based on provider protocol."""
        if self._client is not None:
            return self._client
        if self._client_error is not None:
            return None
        if not self.api_key:
            return None

        saved_env = _clear_proxy_env()
        try:
            if self._protocol == "anthropic":
                self._init_anthropic_client()
            else:
                self._init_openai_client()
        except Exception as e:
            self._client_error = str(e)
        finally:
            _restore_proxy_env(saved_env)
        return self._client

    def _init_anthropic_client(self):
        """Initialize Anthropic SDK client."""
        if not anthropic:
            raise ImportError("anthropic package not installed")
        kwargs: Dict[str, Any] = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        self._client = anthropic.Anthropic(**kwargs)

    def _init_openai_client(self):
        """Initialize OpenAI-compatible SDK client."""
        if not openai:
            raise ImportError("openai package not installed")
        self._client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def _call_api(self, system_prompt: str, messages: List[Dict], max_tokens: int = 4096) -> str:
        """Unified API call dispatcher."""
        if not self.client:
            if self._client_error:
                return f"API connection error: {self._client_error}"
            return self._fallback_response("")

        try:
            if self._protocol == "anthropic":
                return self._call_anthropic(system_prompt, messages, max_tokens)
            else:
                return self._call_openai(system_prompt, messages, max_tokens)
        except Exception as e:
            return f"API error: {e}"

    def _call_anthropic(self, system_prompt: str, messages: List[Dict], max_tokens: int) -> str:
        """Call via Anthropic Messages API."""
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text

    def _call_openai(self, system_prompt: str, messages: List[Dict], max_tokens: int) -> str:
        """Call via OpenAI Chat Completions API."""
        oai_messages = [{"role": "system", "content": system_prompt}]
        oai_messages.extend(messages)
        response = self._client.chat.completions.create(
            model=self.model,
            messages=oai_messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def chat(self, user_message: str, context: Optional[Dict] = None) -> str:
        """Process a user message and return a response."""
        messages = list(self.conversation_history)

        if context:
            user_message = f"[Context: {json.dumps(context)}]\n\n{user_message}"

        messages.append({"role": "user", "content": user_message})

        try:
            assistant_message = self._call_api(SYSTEM_PROMPT, messages)

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
            return self._call_api(INTERPRETATION_PROMPT, [{"role": "user", "content": prompt}], max_tokens=2048)
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
