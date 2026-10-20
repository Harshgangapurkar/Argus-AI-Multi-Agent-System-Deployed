from .llm import complete


def generate_argument(topic: str) -> str:
    return complete(
        "You are ARGUS's Advocate. Make the strongest fair case IN FAVOR "
        "of the proposal. Be precise, identify assumptions, and never invent "
        "statistics, citations, or facts. If the topic is ambiguous, state "
        "your interpretation.",
        f"TOPIC: {topic}\n\n"
        "Present a clear thesis, three brief reasons with supporting logic, "
        "one key assumption, and a concise conclusion. "
        "Do not argue the opposing side. Keep the answer under 350 words.",
        "STRICT OUTPUT RULES:",
        "- Output exactly 3 concise arguments.",
        "- Keep the entire response below 250 words.",
        "- Use short bullet points and no lengthy introduction.",
        "- Include only essential reasoning.",
        "- Finish with one short conclusion.",
        temperature=0.4,
        max_tokens=500,
    )
