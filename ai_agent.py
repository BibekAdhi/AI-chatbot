import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Load API keys from environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider == "Groq":
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set.")
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        llm = ChatOpenAI(model=llm_id)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    try:
        agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=system_prompt
        )

        state = {"messages": [{"role": "user", "content": query}]}
        response = agent.invoke(state)

        messages = response.get("messages", [])
        if messages:
            ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]
            return ai_messages[-1] if ai_messages else "No AI message returned."
        else:
            return "No messages returned from agent."
    except Exception as e:
        print("LangGraph agent error:", e)
        raise e
