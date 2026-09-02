# AI Chatbot - Python LLM Assistant

## 📋 Project Explanation

This project is an **AI-powered chatbot assistant** built with Python that leverages the Groq LLM API to provide intelligent conversational capabilities. The chatbot uses a ReAct (Reasoning and Acting) agent framework that allows it to:

- **Perform natural language conversations** with users
- **Execute custom tools** to accomplish specific tasks
- **Stream responses in real-time** for an interactive experience
- **Handle complex reasoning** by breaking down user requests

### Key Features

- 🤖 **Groq LLM Integration** - Uses Groq's high-performance language models
- 🛠️ **Tool System** - Extensible tool framework for custom functionality
- 💬 **Interactive CLI** - Easy-to-use command-line interface
- ⚡ **Real-time Streaming** - Responses stream as they're generated
- 🔐 **Secure API Key Management** - Environment-based configuration

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Input (CLI)                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         LangChain HumanMessage Processor                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│      ReAct Agent (LanGraph Agent Executor)             │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  Decision Engine - Routes to appropriate tools  │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌──────────┐  ┌──────────┐
   │Calculator│  │Say Hello │  │Groq LLM  │
   │  Tool   │  │   Tool   │  │  Model   │
   └─────────┘  └──────────┘  └──────────┘
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Response Generator & Streamer                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Display Output to User                     │
└─────────────────────────────────────────────────────────┘
```

### Components

| Component | Purpose |
|-----------|---------|
| **ChatGroq** | LLM API client for the Groq language model |
| **ReAct Agent** | Decision-making engine that reasons and acts |
| **Custom Tools** | Calculator and Greeting functions |
| **LanGraph** | Agent orchestration and execution framework |
| **LangChain** | Core utilities for message handling |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Groq API key (get one from [console.groq.com](https://console.groq.com))

### Installation Steps

#### 1. Clone or Download the Project

```bash
cd "AI CHATBOT"
```

#### 2. Create a Virtual Environment

**On Windows (PowerShell):**
```bash
python -m venv .venv
```

**Activate the Virtual Environment:**
```bash
.\.venv\Scripts\Activate
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Verify Virtual Environment is Active

You should see `(.venv)` at the beginning of your terminal prompt.

#### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
# On Windows PowerShell
New-Item -Path .env -ItemType File

# On Windows Command Prompt or macOS/Linux
touch .env
```

Add the following to your `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.6-27b
```

**Note:** Replace `your_groq_api_key_here` with your actual Groq API key from [console.groq.com](https://console.groq.com).

#### 6. Run the Chatbot

```bash
python main.py
```

#### 7. Interact with the Chatbot

Once running, you'll see:
```
Welcome! I'm your PythonAIChatbot assistant. Type 'quit' to exit.
You can ask me to perform calculations or chat with me.

You: 
```

Try these commands:
- `Calculate the sum of 5 and 3` - Uses the calculator tool
- `Say hello to John` - Uses the greeting tool
- `What is the weather like?` - Natural conversation
- `quit` - Exit the program

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `langchain-core` | ≥1.5.2 | Core LangChain utilities |
| `langchain-groq` | ≥1.1.3 | Groq LLM integration |
| `langgraph` | ≥1.2.10 | Agent framework and orchestration |
| `python-dotenv` | ≥1.2.2 | Environment variable management |

---

## 🔧 Deactivating Virtual Environment

When you're done working on the project:

```bash
deactivate
```

---

## 📝 Project Structure

```
AI CHATBOT/
├── main.py              # Main chatbot application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .venv/               # Virtual environment directory (auto-created)
└── README.md            # This file
```

---

## 🛠️ Customization

### Adding New Tools

To add a new tool to the chatbot, follow this pattern in `main.py`:

```python
@tool
def your_tool_name(parameter: type) -> str:
    """Description of what this tool does"""
    # Your implementation here
    return result

# Then add it to the tools list:
tools = [calculator, say_hello, your_tool_name]
```

### Changing the LLM Model

Update the `GROQ_MODEL` in your `.env` file or modify the default in `main.py`:

```python
model_name = os.getenv("GROQ_MODEL", "your_desired_model")
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure virtual environment is activated and dependencies are installed |
| `GROQ_API_KEY not found` | Check your `.env` file and ensure the API key is correctly set |
| Virtual env won't activate | Try using full path: `python -m venv .venv` then activate |
| Port/Connection errors | Verify your internet connection and Groq API availability |

---

## 📄 License

This project is open-source and available for personal and educational use.

---

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

## 📧 Support

For issues or questions, refer to:
- [LangChain Documentation](https://python.langchain.com/)
- [LanGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Groq API Documentation](https://groq.com/)

---

**Happy Chatting! 🎉**
