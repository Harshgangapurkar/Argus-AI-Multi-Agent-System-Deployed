# ARGUS — AI Multi-Agent Debate System

🚀 **Live Demo:** https://argus-ai-multi-agent-system-deployed-harsh.streamlit.app

ARGUS is an AI-powered multi-agent debate system that evaluates a given topic through multiple perspectives. It uses specialized AI agents to build arguments, challenge opposing viewpoints, critically evaluate both sides, and deliver a final judgment.

## 🤖 AI Agents

- **Advocate:** Develops arguments supporting the given topic.
- **Opposition:** Challenges the topic with counterarguments.
- **Critic:** Evaluates both sides based on relevance, logic, evidence, and completeness.
- **Judge:** Analyzes the debate and delivers the final verdict and recommendation.

## ✨ Key Features

- Multi-agent debate workflow with specialized AI roles.
- LLM-powered argument generation and evaluation using the Groq API.
- Structured comparison and scoring of competing arguments.
- Interactive Streamlit interface with expandable results and downloadable debate reports.

## 🛠️ Tech Stack

- **Language:** Python
- **LLM API:** Groq API — OpenAI GPT-OSS 20B
- **Framework:** Streamlit
- **Architecture:** Multi-agent AI system

## ⚙️ Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Harshgangapurkar/Argus-AI-Multi-Agent-System-Deployed.git
   cd Argus-AI-Multi-Agent-System-Deployed
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create `.streamlit/secrets.toml` and add your Groq configuration:

   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   GROQ_MODEL = "openai/gpt-oss-20b"
   ```

4. Launch the application:

   ```bash
   streamlit run app.py
   ```

## 🔐 Security

Store API keys in Streamlit Secrets or environment variables. Never commit API keys or `.streamlit/secrets.toml` to a public repository.

## 👨‍💻 Author

**Harsh Gangapurkar**

[GitHub](https://github.com/Harshgangapurkar) · [Live Application](https://argus-ai-multi-agent-system-deployed-harsh.streamlit.app)

