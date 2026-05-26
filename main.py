import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS ----------
st.markdown(
    """
<style>
    /* Main gradient header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    /* Section headers */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #e2e8f0;
    }
    /* Chat message styling overrides */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.4rem;
    }
    /* Input styling */
    div[data-testid="stChatInput"] input {
        border-radius: 20px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
    }
    /* Better button */
    div.stButton > button {
        border-radius: 20px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] .sidebar-content {
        padding: 1.5rem 1rem;
    }
    /* Divider */
    .custom-divider {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # API Key input with fallback
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="Enter your Groq API key...",
            help="Get your API key at https://console.groq.com",
        )

    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown(
        """
- Ask any question and get AI-powered answers
- Paste long emails for quick summarization
- Conversation history is preserved per session
        """
    )
    # Clear chat button moved to sidebar
    if st.session_state.get("chat_history"):
        if st.button("🗑️ Clear conversation", type="secondary", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown(
        "🔗 [Groq Console](https://console.groq.com)  \n"
        "📖 [Streamlit Docs](https://docs.streamlit.io)"
    )

# ---------- API Key Validation ----------
if not api_key:
    st.warning(
        "🔑 Groq API Key not found.\n\n"
        "Please set your `GROQ_API_KEY` in a `.env` file, "
        "Streamlit secrets, or enter it in the sidebar."
    )
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# ---------- Initialize Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "email_summary" not in st.session_state:
    st.session_state.email_summary = ""

# ---------- Title ----------
st.markdown('<p class="main-header">🤖 AI Personal Assistant</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Powered by Groq · Streamlit</p>',
    unsafe_allow_html=True,
)

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["💬 Chat & Ask", "📧 Summarize Email"])

# ────────────────────────────────────────────
# TAB 1: CHAT & ASK
# ────────────────────────────────────────────
with tab1:
    st.markdown(
        '<p class="section-title">Ask Anything</p>', unsafe_allow_html=True
    )

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask anything..."):
        # Validate non-empty input
        if not prompt.strip():
            st.warning("Please enter a question.")
        else:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    placeholder = st.empty()
                    try:
                        # Build messages: system + last 20 messages from history
                        recent_history = st.session_state.chat_history[-20:]
                        messages = [
                            {
                                "role": "system",
                                "content": "Act like a helpful personal assistant",
                            },
                            *[
                                {"role": m["role"], "content": m["content"]}
                                for m in recent_history
                            ],
                        ]
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=messages,
                            temperature=0.7,
                            max_tokens=512,
                        )
                        answer = response.choices[0].message.content.strip()
                        placeholder.markdown(answer)
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": answer}
                        )
                    except Exception as e:
                        placeholder.error(f"Error communicating with Groq: {str(e)}")

# ────────────────────────────────────────────
# TAB 2: SUMMARIZE EMAIL
# ────────────────────────────────────────────
with tab2:
    st.markdown(
        '<p class="section-title">Summarize Email</p>', unsafe_allow_html=True
    )

    with st.form("email_form", clear_on_submit=True):
        email_text = st.text_area(
            "Email Text",
            placeholder="Paste your email here...",
            height=180,
            label_visibility="collapsed",
        )
        summarize_col1, summarize_col2 = st.columns([1, 5])
        with summarize_col1:
            summarize_submitted = st.form_submit_button(
                "📝 Summarize", type="primary", use_container_width=True
            )

    if summarize_submitted:
        if not email_text.strip():
            st.error("⚠️ Please provide an email to summarize.")
        else:
            with st.spinner("Summarizing..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": "Act like an expert email assistant",
                            },
                            {
                                "role": "user",
                                "content": f"summarize the following email in 2-3 sentences: {email_text}",
                            },
                        ],
                        temperature=0.3,
                        max_tokens=512,
                    )
                    summary = response.choices[0].message.content.strip()
                    st.session_state.email_summary = summary
                except Exception as e:
                    st.error(f"Error communicating with Groq: {str(e)}")

    # Display the last summary
    if st.session_state.email_summary:
        st.markdown("#### 📋 Summary")
        st.info(st.session_state.email_summary)

        if st.button("🗑️ Clear summary", type="secondary"):
            st.session_state.email_summary = ""
            st.rerun()

# ---------- Footer ----------
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p class="footer">Built with ❤️ using Streamlit & Groq</p>',
    unsafe_allow_html=True,
)
