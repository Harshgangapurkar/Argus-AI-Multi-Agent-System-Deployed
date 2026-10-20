
import re

from .llm import complete


def _has_valid_winner(text: str) -> bool:
    """Require an explicit FOR or AGAINST winner."""
    return bool(
        re.search(
            r"(?im)^\s*(?:\*\*)?Winner\s*:\s*"
            r"(?:\*\*)?\s*(FOR|AGAINST)\b",
            text,
        )
    )


def generate_verdict(
    topic: str,
    pro_argument: str,
    con_argument: str,
    critique: str,
) -> str:
    system_prompt = """
You are ARGUS's decisive final judge.
You MUST choose exactly one winner: FOR or AGAINST.
Never return a balanced, tied, or inconclusive verdict.
Compare argument quality, logic, relevance, evidence,
assumptions, and responses to objections.
Use the critic's review as input, not unquestionable authority.
Do not invent facts or claim external fact-checking.
Be concise and acknowledge uncertainty without refusing to choose.
"""

    user_prompt = f"""TOPIC: {topic}

ADVOCATE — FOR:
{pro_argument}

OPPOSITION — AGAINST:
{con_argument}

CRITIC'S REVIEW:
{critique}

DECISION:
Choose the side with the stronger overall argument.

Compare logic, relevance, evidence, assumptions, and weaknesses.
Do not reward length or confidence alone.
Missing evidence does not automatically mean a tie.

If the sides appear equally strong, break the tie by preferring:
1. Fewer unsupported assumptions.
2. Stronger logical reasoning.
3. Better responses to important objections.
4. Greater relevance to the topic.

You must choose FOR or AGAINST even when evidence is incomplete.
This is a judgment of the submitted arguments, not proof of
objective truth.

OUTPUT FORMAT:

## VERDICT
Winner: FOR or AGAINST
Give the main reason in one or two sentences.

## SCORES
FOR: X/10 — brief reason.
AGAINST: X/10 — brief reason.

## KEY REASONS
Give the two strongest reasons supporting the winner.

## WHAT COULD CHANGE THE VERDICT
State the most important missing evidence, if any.

## FINAL RECOMMENDATION
Give a concise recommendation consistent with the winner.

STRICT RULES:
- Stay within 500 completion tokens.
- The winner must be exactly FOR or AGAINST.
- Never use "balanced" or "inconclusive" as the verdict.
- Do not invent facts, statistics, or citations.
- Keep all sections concise.
"""

    result = complete(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.1,
        max_tokens=500,
    )

    if _has_valid_winner(result):
        return result

    # One retry if the model ignored the mandatory winner format.
    retry_prompt = f"""TOPIC: {topic}

FOR argument:
{pro_argument[:2500]}

AGAINST argument:
{con_argument[:2500]}

Critic:
{critique[:1500]}

Your previous response did not provide a valid winner.

Choose exactly one: FOR or AGAINST.
Compare the arguments and use the stronger reasoning as the
tie-breaker if needed. Do not return a balanced verdict.

Output no more than 200 words in this format:

## VERDICT
Winner: FOR or AGAINST
Reason: ...

## SCORES
FOR: X/10 — reason.
AGAINST: X/10 — reason.

## KEY REASONS
Brief explanation.

## WHAT COULD CHANGE THE VERDICT
One brief sentence.

## FINAL RECOMMENDATION
One brief sentence.

Never invent facts or citations.
"""

    result = complete(
        system_prompt=(
            "You are ARGUS's final judge. Output an explicit "
            "Winner: FOR or Winner: AGAINST. Never return a tie."
        ),
        user_prompt=retry_prompt,
        temperature=0.0,
        max_tokens=500,
    )

    if not _has_valid_winner(result):
        raise RuntimeError(
            "Judge failed to produce a valid FOR/AGAINST winner "
            "after one retry. Please retry the debate."
        )

    return result
