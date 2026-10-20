
from .llm import complete


def critique_arguments(
    topic: str,
    pro_argument: str,
    con_argument: str,
) -> str:
    prompt = f"""TOPIC: {topic}

ADVOCATE — CASE FOR:
{pro_argument}

OPPOSITION — CASE AGAINST:
{con_argument}

Evaluate both arguments fairly and independently.

REQUIRED OUTPUT:

## 1. Comparative Scorecard
Create a Markdown table with these columns:
| Criterion | Advocate Score | Opposition Score |

Include exactly four rows:
- Relevance
- Logical validity
- Evidence and grounding
- Completeness

Score each side from 1 to 10. Use the same standards
for both sides. Do not invent evidence.

## 2. Strongest Points
- Advocate: one strongest supported point.
- Opposition: one strongest supported point.

## 3. Weakest Points
- Advocate: one key weakness.
- Opposition: one key weakness.

## 4. Missing Evidence
Briefly identify important assumptions or missing information.

## 5. Comparative Assessment
State which argument is better supported, or whether
the available information is insufficient.

STRICT OUTPUT RULES:
- Stay within the 500-token completion budget.
- Keep the entire response concise.
- Use short bullet points and brief sentences.
- Avoid repetition and lengthy explanations.
- Do not leave scorecard cells blank.
- Do not invent facts, statistics, citations, or evidence.
- Do not claim external fact-checking.
- Do not deliver the final verdict; the Judge does that.
- Evaluate the supplied arguments, not personal preferences.
"""

    return complete(
        system_prompt=(
            "You are ARGUS's impartial debate critic. "
            "Evaluate both sides symmetrically and follow "
            "the requested output structure. Be concise."
        ),
        user_prompt=prompt,
        temperature=0.1,
        max_tokens=500,
    )
