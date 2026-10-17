from .llm import complete


def generate_argument(topic: str) -> str:
    return complete(
        "You are ARGUS's Opposition. Make the strongest fair case AGAINST the proposal. "
        "Challenge assumptions, identify risks and trade-offs, and do not invent statistics, "
        "citations, or facts. If the topic is ambiguous, state your interpretation.",
        f"TOPIC: {topic}\n\nPresent a clear thesis, three distinct counterarguments with reasoning, "
        "the most important assumption, and a concise conclusion. Do not argue in favor.",
        temperature=0.4, max_tokens=1000,
    )
