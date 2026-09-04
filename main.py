
import os
import warnings

import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


# ============================================================
# CONFIGURATION
# ============================================================

warnings.filterwarnings("ignore")
load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_tool" not in st.session_state:
    st.session_state.active_tool = None


# ============================================================
# PROFESSIONAL DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #070b14;
        color: #f8fafc;
    }

    /* Main content */
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #090e1a;
        border-right: 1px solid #20283d;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem;
    }

    /* All normal text */
    p, label {
        color: #d7deea;
    }

    /* Headings */
    h1, h2, h3 {
        color: #ffffff !important;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton button {
        background: #101727;
        color: #dce4f2;
        border: 1px solid #252f46;
        border-radius: 10px;
        min-height: 44px;
        font-weight: 600;
        text-align: left;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: #171d32;
        color: #ffffff;
        border-color: #6955d9;
    }

    /* Normal buttons */
    .stButton button {
        background: #111827;
        color: #e5e7eb;
        border: 1px solid #303b55;
        border-radius: 10px;
        font-weight: 600;
    }

    .stButton button:hover {
        background: #191f35;
        color: white;
        border-color: #6955d9;
    }

    /* Primary buttons */
    .stButton button[kind="primary"] {
        background: #5b45c7;
        color: white;
        border: 1px solid #755fe0;
    }

    .stButton button[kind="primary"]:hover {
        background: #6d55df;
    }

    /* Text input */
    .stTextInput input {
        background: #0e1524 !important;
        color: white !important;
        border: 1px solid #29354e !important;
        border-radius: 10px !important;
    }

    .stTextInput input:focus {
        border-color: #6955d9 !important;
    }

    /* Number input */
    .stNumberInput input {
        background: #0e1524 !important;
        color: white !important;
        border: 1px solid #29354e !important;
        border-radius: 10px !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: #0e1524;
        border: 1px solid #222c42;
        border-radius: 14px;
        padding: 12px 15px;
        margin-bottom: 10px;
    }

    [data-testid="stChatMessageContent"] {
        color: #e5e7eb;
    }

    /* Chat input */
    [data-testid="stChatInput"] > div {
        background: #0e1524 !important;
        border: 1px solid #5b45c7 !important;
        border-radius: 14px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: white !important;
        background: transparent !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #68758c !important;
    }

    [data-testid="stChatInput"] button {
        background: #5b45c7 !important;
        border-radius: 9px !important;
    }

    /* Divider */
    hr {
        border-color: #20283d !important;
    }

    /* Info */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOOLS
# ============================================================

@tool
def calculator(a: float, b: float) -> str:
    """Add two numbers together."""
    return f"The sum of {a} and {b} is {a + b}"


@tool
def say_hello(name: str) -> str:
    """Generate a friendly greeting."""
    return f"Hello {name}, I hope you are well today!"


# ============================================================
# INITIALIZE AI AGENT
# ============================================================

@st.cache_resource
def initialize_agent():

    groq_key = os.getenv("GROQ_API_KEY")

    model_name = os.getenv(
        "GROQ_MODEL",
        "qwen/qwen3.6-27b"
    )

    if not groq_key:
        return None, model_name, "GROQ_API_KEY is not configured."

    try:

        model = ChatGroq(
            model=model_name,
            temperature=0,
            api_key=groq_key
        )

        tools = [
            calculator,
            say_hello
        ]

        agent_executor = create_react_agent(
            model,
            tools
        )

        return agent_executor, model_name, None

    except Exception as e:

        return None, model_name, str(e)


agent_executor, model_name, initialization_error = initialize_agent()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # Brand
    st.title("🤖 AI Assistant")

    st.caption("Your intelligent workspace")

    st.divider()

    # Model
    st.caption("AI MODEL")

    st.info(
        f"⚡ Active Model\n\n{model_name}"
    )

    # Status
    st.caption("SYSTEM STATUS")

    if initialization_error:

        st.error("🔴 AI Agent Offline")

    else:

        st.success("🟢 AI Agent Online")

    st.divider()

    # Tools
    st.caption("AVAILABLE TOOLS")

    if st.button(
        "🧮  Calculator",
        use_container_width=True
    ):

        if st.session_state.active_tool == "calculator":
            st.session_state.active_tool = None
        else:
            st.session_state.active_tool = "calculator"

        st.rerun()

    if st.button(
        "👋  Greeting Assistant",
        use_container_width=True
    ):

        if st.session_state.active_tool == "greeting":
            st.session_state.active_tool = None
        else:
            st.session_state.active_tool = "greeting"

        st.rerun()

    st.divider()

    # Conversation
    st.caption("CONVERSATION")

    if st.button(
        "➕  New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.active_tool = None

        st.rerun()

    if st.button(
        "🗑️  Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("ABOUT")

    st.caption(
        "AI Assistant powered by Groq, "
        "LangChain and LangGraph."
    )


# ============================================================
# ERROR CHECK
# ============================================================

if initialization_error:

    st.error(
        "Unable to initialize the AI Assistant."
    )

    st.warning(initialization_error)

    st.stop()


# ============================================================
# MAIN TITLE
# ============================================================

title_col, model_col = st.columns([4, 1])

with title_col:

    st.title("AI Assistant")

    st.caption(
        "A smart assistant for questions, calculations, "
        "greetings and everyday tasks."
    )

with model_col:

    st.write("")

    st.info(
        f"⚡ {model_name}"
    )


st.divider()


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.subheader("Welcome! 👋")

    st.write(
        "How can I help you today?"
    )

    st.write("")

    # Tool cards using Streamlit columns
    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("🧮 Calculator")

            st.caption(
                "Quickly add two numbers together."
            )

            if st.button(
                "Open Calculator →",
                key="open_calculator",
                use_container_width=True
            ):

                st.session_state.active_tool = "calculator"

                st.rerun()

    with col2:

        with st.container(border=True):

            st.subheader("👋 Greeting Assistant")

            st.caption(
                "Generate a friendly personalized greeting."
            )

            if st.button(
                "Open Greeting Assistant →",
                key="open_greeting",
                use_container_width=True
            ):

                st.session_state.active_tool = "greeting"

                st.rerun()


# ============================================================
# CALCULATOR
# ============================================================

if st.session_state.active_tool == "calculator":

    st.divider()

    st.subheader("🧮 Calculator")

    st.caption(
        "Enter two numbers to calculate their sum."
    )

    col1, col2, col3 = st.columns(
        [1, 1, 0.7]
    )

    with col1:

        number_a = st.number_input(
            "First number",
            value=0.0,
            step=1.0,
            key="calculator_a"
        )

    with col2:

        number_b = st.number_input(
            "Second number",
            value=0.0,
            step=1.0,
            key="calculator_b"
        )

    with col3:

        st.write("")

        st.write("")

        if st.button(
            "Calculate",
            type="primary",
            use_container_width=True
        ):

            result = calculator.invoke(
                {
                    "a": number_a,
                    "b": number_b
                }
            )

            st.success(result)


# ============================================================
# GREETING ASSISTANT
# ============================================================

elif st.session_state.active_tool == "greeting":

    st.divider()

    st.subheader("👋 Greeting Assistant")

    st.caption(
        "Enter your name to generate a friendly greeting."
    )

    col1, col2 = st.columns(
        [2, 0.7]
    )

    with col1:

        user_name = st.text_input(
            "Your name",
            placeholder="Enter your name...",
            key="greeting_name"
        )

    with col2:

        st.write("")

        st.write("")

        if st.button(
            "Generate Greeting",
            type="primary",
            use_container_width=True
        ):

            if user_name.strip():

                result = say_hello.invoke(
                    {
                        "name": user_name.strip()
                    }
                )

                st.success(result)

            else:

                st.warning(
                    "Please enter your name first."
                )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        avatar = "👤"

    else:

        avatar = "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Type your message here..."
)


# ============================================================
# PROCESS MESSAGE
# ============================================================

if user_input:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(user_input)


    # AI response
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        response_placeholder = st.empty()

        full_response = ""

        try:

            for chunk in agent_executor.stream(
                {
                    "messages": [
                        HumanMessage(
                            content=user_input
                        )
                    ]
                }
            ):

                if "agent" not in chunk:
                    continue

                agent_data = chunk["agent"]

                if "messages" not in agent_data:
                    continue

                messages = agent_data["messages"]

                if not messages:
                    continue

                message = messages[-1]

                content = message.content

                if isinstance(content, str):

                    if content.strip():

                        full_response = content

                        response_placeholder.markdown(
                            full_response
                        )

                elif isinstance(content, list):

                    text_parts = []

                    for item in content:

                        if isinstance(item, dict):

                            if "text" in item:

                                text_parts.append(
                                    item["text"]
                                )

                    text = "".join(text_parts)

                    if text.strip():

                        full_response = text

                        response_placeholder.markdown(
                            full_response
                        )


            if not full_response:

                full_response = (
                    "I couldn't generate a response. "
                    "Please try again."
                )

                response_placeholder.warning(
                    full_response
                )


        except Exception as e:

            full_response = (
                "An error occurred while generating "
                "the response."
            )

            response_placeholder.error(
                full_response
            )

            st.caption(
                str(e)
            )


    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    st.rerun()

