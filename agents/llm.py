
"""Shared Groq client and reliable completion helper."""

import os
from functools import lru_cache

import streamlit as st
from groq import Groq

DEFAULT_MODEL = "openai/gpt-oss-20b"


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
    max_tokens: int = 1200,
) -> str:
    """Generate a completion and detect empty or truncated responses."""

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

    # Never silently accept a response cut off by the token limit.
    if finish_reason == "length":
        raise RuntimeError(
            f"Model '{model}' exhausted its completion budget "
            f"({max_tokens} tokens). Shorten the prompt or adjust "
            "the budget for this agent."
        )

    if isinstance(content, str) and content.strip():
        return content.strip()

    raise RuntimeError(
        f"Model '{model}' returned no usable text. "
        f"Finish reason: {finish_reason}."
    )
