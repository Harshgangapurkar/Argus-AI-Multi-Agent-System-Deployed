
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

Create a Markdown table with exactly these columns:

| Criterion | Advocate Score | Advocate Strength | Advocate Weakness | Opposition Score | Opposition Strength | Opposition Weakness |
|---|---|---|---|---|---|---|

Include four rows:
- Relevance
- Logical validity
- Evidence and grounding
- Completeness

Rules for the table:
- Score each side from 1 to 10.
- EVERY cell must contain meaningful content.
- Never leave a cell blank.
- If information is missing, explicitly write "Not established in the argument."
- Evaluate the Advocate and Opposition independently using the same standards.
- Do not invent facts, statistics, citations, or evidence.
- Keep each cell concise but specific to the supplied arguments.

## 2. Strongest Points
- Advocate: identify its strongest supported point.
- Opposition: identify its strongest supported point.

## 3. Weakest Points
- Advocate: identify its weakest reasoning or unsupported claim.
- Opposition: identify its weakest reasoning or unsupported claim.

## 4. Assumptions and Missing Evidence
Identify the important assumptions made by each side and what information is missing.

## 5. Comparative Assessment
Explain which argument is better supported, or whether the evidence is insufficient to distinguish them.

IMPORTANT:
- Evaluate the actual arguments supplied, not which position you personally prefer.
- Do not assume the Advocate wins simply because its argument is longer.
- Do not assume the Opposition wins merely by criticizing the framing.
- If either argument is incomplete, say so explicitly.
- Do not deliver the final verdict; that is the Judge's responsibility.
- Do not claim to have fact-checked information externally.
"""

    return complete(
        system_prompt=(
            "You are ARGUS's impartial debate critic. "
            "You must assess both sides symmetrically. "
            "Follow the requested output structure exactly. "
            "Never omit a table cell. Never invent evidence."
        ),
        user_prompt=prompt,
        temperature=0.1, max_tokens=1000,
    )
