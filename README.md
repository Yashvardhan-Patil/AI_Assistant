# 🤖 AI Personal Assistant

A smart AI-powered personal assistant built with **Streamlit** and **Groq's Llama 3.1** model.

## Features

- **💬 Chat & Ask** – Ask any question and get AI-powered answers with conversation history
- **📧 Summarize Email** – Paste long emails for instant 2–3 sentence summaries
- **⚙️ Sidebar config** – Set your Groq API key or use environment variables
- **🎨 Polished UI** – Gradient headers, custom styling, responsive layout

## Tech Stack

- [Streamlit](https://streamlit.io) – UI framework
- [Groq API](https://console.groq.com) – LLM inference (Llama 3.1 8B)
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Environment management

## Getting Started

### 1. Clone & install

```bash
git clone <repo-url>
cd AI_Assistant

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

### 2. Set your API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=gsk_your_key_here
```

Or set it as a [Streamlit secret](https://docs.streamlit.io/develop/api-reference/runtime/secrets) when deploying.

### 3. Run locally

```bash
streamlit run main.py
```

## Deployment

Designed for easy deployment on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and deploy
4. Add your `GROQ_API_KEY` in **Settings → Secrets**

---

Built with ❤️ using Streamlit & Groq
