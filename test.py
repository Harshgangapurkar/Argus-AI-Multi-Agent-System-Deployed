
import streamlit as st

key = st.secrets.get("GROQ_API_KEY", "")

print("Key exists:", bool(key))
print("Starts with gsk_:", key.startswith("gsk_"))
print("Key length:", len(key))
