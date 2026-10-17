"""Debate orchestration: independent opening arguments run concurrently."""
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from agents.advocate import generate_argument as generate_pro_argument
from agents.opposition import generate_argument as generate_con_argument
from agents.critic import critique_arguments
from agents.judge import generate_verdict


def run_debate(topic: str) -> dict:
    topic = " ".join(topic.split()).strip()
    if not topic:
        raise ValueError("Enter a topic before starting the debate.")
    if len(topic) > 1200:
        raise ValueError("Please keep the topic under 1,200 characters.")

    start = perf_counter()
    # These calls are independent; parallel execution reduces wall-clock latency.
    with ThreadPoolExecutor(max_workers=2) as pool:
        pro_future = pool.submit(generate_pro_argument, topic)
        con_future = pool.submit(generate_con_argument, topic)
        pro_argument = pro_future.result()
        con_argument = con_future.result()

    critique = critique_arguments(topic, pro_argument, con_argument)
    verdict = generate_verdict(topic, pro_argument, con_argument, critique)
    return {
        "topic": topic,
        "for": pro_argument,
        "against": con_argument,
        "critique": critique,
        "verdict": verdict,
        "elapsed_seconds": round(perf_counter() - start, 2),
        "model": "Configured by app owner",
    }
