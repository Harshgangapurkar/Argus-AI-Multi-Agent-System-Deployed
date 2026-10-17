# ARGUS — Multi-Agent AI Debate Engine

ARGUS uses four roles: Advocate, Opposition, Critic, and Judge. The two opening arguments run concurrently; the critic and judge then run in sequence because each depends on the previous outputs.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with your own values:

   ```toml
   GROQ_API_KEY = "your-key"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   ```

4. Start the app: `streamlit run app.py`

Do not commit `.streamlit/secrets.toml`. The example file contains a placeholder only.

## Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository (without `.venv`, `.git`, or real secrets).
2. In Streamlit Community Cloud, create an app from that repository and select `app.py` as the entry point.
3. In **App settings → Secrets**, add:

   ```toml
   GROQ_API_KEY = "your-real-key"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   ```

4. Deploy. Visitors do not enter an API key; server-side calls use the key configured by the owner.

## Performance and safety notes

- Advocate and Opposition run concurrently, reducing wait time compared with sequential calls. Critic and Judge remain sequential.
- Reuses one API client; requests have timeouts and limited retries.
- Prompts ask agents not to invent evidence and the Judge to disclose uncertainty.
- Input is limited to 1,200 characters and the UI limits each browser session to 10 debates. This is a lightweight guardrail, **not** a robust public rate limiter: session limits can be reset and do not coordinate across users. For a public launch, add shared rate limiting/authentication and provider-side spend limits.
- The app's API key remains server-side, but visitors' usage consumes the owner's provider quota and may incur charges.
- Model names can change at the provider. If the default model is unavailable on your account, set `GROQ_MODEL` to a currently supported Groq model in Streamlit Secrets.
