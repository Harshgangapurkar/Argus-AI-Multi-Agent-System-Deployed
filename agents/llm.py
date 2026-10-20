
"""Shared Groq client and reliable completion helper."""

import os
from functools import lru_cache

import streamlit as st
from groq import Groq

DEFAULT_MODEL = "openai/gpt-oss-20b"
DEFAULT_MAX_TOKENS = 500


def get_setting(name: str, default: str = "") -> str:
    """Read settings from Streamlit Secrets or environment variables."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""

    return str(value or os.getenv(name, default)).strip()


@lru_cache(maxsize=1)
def get_client() -> Groq:
    """Create one reusable server-side Groq client."""
    api_key = get_setting("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Configure it in "
            ".streamlit/secrets.toml or Streamlit Cloud Secrets."
        )

    return Groq(
        api_key=api_key,
        timeout=60.0,
        max_retries=2,
    )


def complete(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.3,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Generate text, rejecting empty or truncated responses."""

    if not isinstance(system_prompt, str) or not system_prompt.strip():
        raise ValueError("system_prompt must be a non-empty string.")

    if not isinstance(user_prompt, str) or not user_prompt.strip():
        raise ValueError("user_prompt must be a non-empty string.")

    if not isinstance(max_tokens, int) or not 1 <= max_tokens <= 500:
        raise ValueError("max_tokens must be between 1 and 500.")

    client = get_client()
    model = get_setting("GROQ_MODEL", DEFAULT_MODEL)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_completion_tokens=max_tokens,
            reasoning_effort="low",
        )

    except Exception as exc:
        raise RuntimeError(
            f"Groq request failed ({type(exc).__name__}): {exc}"
        ) from exc

    if not response.choices:
        raise RuntimeError(
            f"Groq returned no choices for model '{model}'."
        )

    choice = response.choices[0]
    content = choice.message.content
    finish_reason = choice.finish_reason or "unknown"

    if finish_reason == "length":
        raise RuntimeError(
            f"Model '{model}' reached its {max_tokens}-token "
            "completion limit. Shorten the prompt or output format."
        )

    if not isinstance(content, str) or not content.strip():
        raise RuntimeError(
            f"Model '{model}' returned no usable text. "
            f"Finish reason: {finish_reason}."
        )

    return content.strip()
