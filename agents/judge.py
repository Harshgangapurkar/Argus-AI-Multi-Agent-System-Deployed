from .llm import complete


def generate_verdict(topic: str, pro_argument: str, con_argument: str, critique: str) -> str:
    prompt = f"""TOPIC: {topic}

ADVOCATE:
{pro_argument}

OPPOSITION:
{con_argument}

CRITIC'S REVIEW:
{critique}

Deliver the final decision using these headings:
1. VERDICT — FOR is stronger / AGAINST is stronger / balanced or conditional.
2. SCORES — score each side 1–10 and give a one-line justification for each.
3. REASONS — compare the best arguments and the key weaknesses directly.
4. WHAT WOULD CHANGE THE VERDICT — name the key evidence or assumptions that could change it.
5. FINAL RECOMMENDATION — concise, practical and conditional where appropriate.

Judge argument quality and support, not rhetorical confidence. The critic is input, not authority:
correctly reject any unsupported scoring or reasoning. Do not invent evidence or claim external fact-checking.
If the topic depends on facts not supplied, make that limitation explicit."""
    return complete(
        "You are ARGUS's final judge. Be independent, balanced, transparent about uncertainty, "
        "and willing to return a conditional verdict. Never invent evidence.",
        prompt, temperature=0.1, max_tokens=900,
    )
