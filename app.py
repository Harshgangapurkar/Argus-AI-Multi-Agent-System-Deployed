
import streamlit as st
from core.debate import run_debate
from agents.llm import get_client



st.set_page_config(page_title="ARGUS | AI Debate Engine", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 1.5rem 1.7rem; border: 1px solid rgba(128,128,128,.25); border-radius: 18px; margin-bottom: 1rem;}
.hero h1 {margin: 0; letter-spacing: .04em;}
.muted {opacity: .78;}
</style>
<div class="hero">
<h1>⚖️ ARGUS</h1>
<p class="muted">Multi-agent AI debate & decision engine</p>
<p>Two opposing agents build their cases. A critic stress-tests both. An independent judge delivers a reasoned verdict.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("How ARGUS works")
    st.markdown("**01 · Advocate** — argues in favor\n\n**02 · Opposition** — argues against\n\n**03 · Critic** — scores both arguments\n\n**04 · Judge** — delivers the final verdict")
    st.caption("The model API key is configured by the app owner and is never requested from visitors.")
    st.caption("AI-generated judgments can be wrong. Treat them as structured analysis, not professional advice.")

if "debate_count" not in st.session_state:
    st.session_state.debate_count = 0

with st.form("debate_form"):
    topic = st.text_area(
        "What should ARGUS debate?",
        placeholder="Example: Should AI-generated content require mandatory labeling?",
        height=110,
        max_chars=1200,
        help="Use a focused question or proposal for the most useful debate.",
    )
    submitted = st.form_submit_button("⚖️ Start debate", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Enter a topic to start the debate.")
    elif st.session_state.debate_count >= 10:
        st.warning("You've reached 10 debates in this session. Refreshing the page will reset this session limit; for public launch, add a shared rate limiter to prevent API abuse.")
    else:
        try:
            # Validate owner secret before showing the progress UI.
            get_client()
            with st.status("ARGUS is running the four-stage debate…", expanded=True) as status:
                st.write("1. Advocate and Opposition are preparing their arguments in parallel.")
                st.write("2. Critic evaluates the strengths and weaknesses of both sides.")
                st.write("3. Judge compares the arguments and produces a verdict.")
                result = run_debate(topic)
                status.update(label="Debate complete", state="complete", expanded=False)
            st.session_state.debate_count += 1
            st.session_state.last_result = result
        except Exception as exc:
            # Do not display exception internals that might contain implementation details.
            st.error(f"ARGUS could not complete this debate: {exc}")

result = st.session_state.get("last_result")
if result:
    st.divider()
    st.subheader("Final judgment")
    st.markdown(f"**Topic:** {result['topic']}")
    st.markdown(result["verdict"])
    left, right = st.columns(2, gap="large")
    with left:
        with st.expander("🟢 Advocate — case FOR", expanded=True):
            st.markdown(result["for"])
    with right:
        with st.expander("🔴 Opposition — case AGAINST", expanded=True):
            st.markdown(result["against"])
    with st.expander("🧠 Critic's evaluation", expanded=True):
        st.markdown(result["critique"])
    st.caption(f"Completed in {result['elapsed_seconds']} seconds · Four-agent pipeline")
    st.download_button(
        "Download debate report (.md)",
        data=(f"# ARGUS Debate Report\n\n## Topic\n{result['topic']}\n\n"
              f"## Final Judgment\n{result['verdict']}\n\n## Advocate\n{result['for']}\n\n"
              f"## Opposition\n{result['against']}\n\n## Critic\n{result['critique']}\n"),
        file_name="argus_debate_report.md",
        mime="text/markdown",
    )
