from .llm import complete


def generate_argument(topic: str) -> str:
    return complete(
        "You are ARGUS's Advocate. Make the strongest fair case IN FAVOR of the proposal. "
        "Be precise, identify assumptions, and do not invent statistics, citations, or facts. "
        "If the topic is ambiguous, state your interpretation.",
        f"TOPIC: {topic}\n\nPresent a clear thesis, three distinct reasons with supporting logic, "
        "the most important assumption, and a concise conclusion. Do not argue the opposing side.",
        temperature=0.4, max_tokens=1000,
    )
