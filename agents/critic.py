
from .llm import complete


def critique_arguments(
    topic: str,
    pro_argument: str,
    con_argument: str,
) -> str:
    system_prompt = """
You are ARGUS's impartial debate critic.
Evaluate both sides fairly and independently using the same standards.
Do not favor a side because of its position or writing style.
Never invent evidence or claim external fact-checking.
Your role is to analyze arguments, not deliver the final verdict.
"""

    user_prompt = f"""TOPIC: {topic}

ADVOCATE — FOR:
{pro_argument}

OPPOSITION — AGAINST:
{con_argument}

Evaluate the actual arguments supplied.

## 1. Scorecard
Use this table:
| Criterion | FOR (1-10) | AGAINST (1-10) |
|---|---:|---:|
| Relevance | | |
| Logical validity | | |
| Evidence and grounding | | |
| Completeness | | |

Score each side independently using the same standards.
Scores must be integers from 1 to 10.

## 2. Strongest Points
Identify one strongest point from each side.

## 3. Weakest Points
Identify one important weakness from each side.

## 4. Missing Evidence
Briefly identify important unsupported assumptions or missing data.

## 5. Comparative Assessment
State which argument is better supported overall and why.
If the arguments are close, explain the key difference rather
than automatically declaring them balanced.

STRICT RULES:
- Stay within 500 completion tokens.
- Keep every section concise.
- Never leave scorecard cells blank.
- Do not invent facts, statistics, or citations.
- Do not deliver the final verdict; the Judge decides.
"""

    return complete(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.1,
        max_tokens=500,
    )
