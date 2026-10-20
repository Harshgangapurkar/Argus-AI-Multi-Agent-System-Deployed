
from .llm import complete


def generate_argument(topic: str) -> str:
    system_prompt = """
You are ARGUS's Advocate. Make the strongest fair case FOR
the proposal. Be precise and logical. Never invent facts,
statistics, or citations. Do not argue the opposing side.
"""

    user_prompt = f"""TOPIC: {topic}

Present:
1. A clear thesis.
2. Exactly three concise arguments with supporting logic.
3. One key assumption.
4. A short conclusion.

STRICT OUTPUT RULES:
- Keep the response concise and within 500 completion tokens.
- Use short bullet points and brief sentences.
- Avoid lengthy introductions and repetition.
- Do not invent facts, statistics, or citations.
- Finish the requested structure within the available budget.
"""

    return complete(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.4,
        max_tokens=500,
    )
