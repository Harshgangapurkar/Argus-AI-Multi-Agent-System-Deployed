
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
        "STRICT OUTPUT RULES:\n",
        "- Keep the response within 500 generated tokens.\n",
        "- Use exactly three concise counterarguments.\n",
        "- Prefer short bullet points over long paragraphs.\n",
        "- Include only essential reasoning; avoid repetition.\n",
        "- Do not invent facts, statistics, or citations.\n",
        "- Finish the response with a concise conclusion.",
        temperature=0.4,
        max_tokens=500,
    )
