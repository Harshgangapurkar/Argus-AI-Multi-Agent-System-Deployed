
from .llm import complete


def generate_verdict(
    topic: str,
    pro_argument: str,
    con_argument: str,
    critique: str,
) -> str:
    prompt = f"""TOPIC: {topic}

ADVOCATE — CASE FOR:
{pro_argument}

OPPOSITION — CASE AGAINST:
{con_argument}

CRITIC'S REVIEW:
{critique}

YOUR TASK:
Make a decisive final decision. ARGUS must select exactly one
winner: FOR or AGAINST. Do not return "balanced", "both sides
win", "neither side", or an inconclusive verdict.

DECISION RULES:
1. Evaluate logical validity, relevance, evidence, assumptions,
   completeness, and responses to opposing arguments.
2. Use the Critic's review as supporting input, not unquestionable
   authority. Correctly reject unsupported criticism or scores.
3. Compare the strongest arguments directly. Do not reward an
   argument simply because it is longer or more confident.
4. Select FOR if the Advocate's case is better supported overall.
   Select AGAINST if the Opposition's case is better supported overall.
5. If both sides appear equally strong, use a tie-breaker:
   - Prefer the side with fewer unsupported assumptions.
   - Then prefer the side with stronger logical reasoning.
   - Then prefer the side that addresses more important objections.
   - If still tied, select the side with the stronger argument
     directly relevant to the topic.
6. Never choose randomly or favor a side just because it is FOR
   or AGAINST.
7. Missing evidence does not automatically make the debate balanced.
   Evaluate the arguments that were actually supplied.
8. Do not invent facts, statistics, citations, or evidence.
   State important uncertainty briefly, but still select a winner.

REQUIRED OUTPUT:

## 1. VERDICT
Winner: FOR or AGAINST
State the main reason in 1-2 sentences.

## 2. SCORES
FOR: X/10 — brief justification.
AGAINST: X/10 — brief justification.

## 3. KEY REASONS
Give the three most important reasons supporting your decision.
Mention the winning side's strongest point and the losing side's
most important weakness.

## 4. WHAT COULD CHANGE THE VERDICT
Name the key missing evidence or assumption that could change
the decision. If none is significant, say so briefly.

## 5. FINAL RECOMMENDATION
Give a concise, practical recommendation consistent with the verdict.

STRICT OUTPUT RULES:
- Stay within the 500-token completion budget.
- Choose exactly one winner: FOR or AGAINST.
- Never use "balanced" or "inconclusive" as the final verdict.
- Be decisive without overstating the available evidence.
- Keep every section concise and avoid repetition.
"""

    return complete(
        system_prompt=(
            "You are ARGUS's decisive final judge. Your responsibility "
            "is to select one winner based on comparative argument "
            "quality. Always choose FOR or AGAINST, using the specified "
            "tie-breaker when necessary. Never return a balanced verdict. "
            "Be fair, evidence-conscious, concise, and transparent "
            "about uncertainty."
        ),
        user_prompt=prompt,
        temperature=0.1,
        max_tokens=500,
    )
