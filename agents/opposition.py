
from .llm import complete


def generate_argument(topic: str) -> str:
    return complete(
        "You are ARGUS's Opposition. Make the strongest fair case AGAINST "
        "the proposal. Challenge assumptions and identify risks and trade-offs. "
        "Never invent statistics, citations, or facts. "
        "If the topic is ambiguous, state your interpretation.",
        f"TOPIC: {topic}\n\n"
        "Present a clear thesis, three brief counterarguments with supporting "
        "logic, one key assumption, and a concise conclusion. "
        "Do not argue in favor. Keep the answer under 350 words.",
        temperature=0.4,
        max_tokens=900,
    )
