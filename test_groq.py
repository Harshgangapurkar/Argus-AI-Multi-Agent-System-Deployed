
import streamlit as st
from groq import Groq

st.title("ARGUS - Groq Connection Test")

try:
    api_key = st.secrets["GROQ_API_KEY"].strip()
    model_name = st.secrets["GROQ_MODEL"]

    client = Groq(api_key=api_key)

    with st.spinner("Testing Groq model..."):
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": "Give one argument for online education."
                }
            ],
            max_completion_tokens=200,
        )

    st.success("Groq authentication and model test successful!")
    st.write("Model:", model_name)
    st.write("Response:")
    st.write(response.choices[0].message.content)

except Exception as e:
    st.error(f"Groq test failed: {type(e).__name__}")
    st.write(str(e))
