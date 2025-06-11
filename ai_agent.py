import os
import json

# SETUP API KEYS FOR Groq, OpenAI, and Tavily
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# SETUP LLM and TOOLS
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

search_tool = TavilySearchResults(max_results=2)

# SETUP AI AGENT WITH SEARCH TOOL FUNCTIONALITY
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt = "Act as an AI chatbot who is smart and friendly"


def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)

    tools=[TavilySearchResults(max_results=2)] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt 
)

    # Query setup
   # query = "Tell me about the trends in crypto markets"
    state = {"messages": [{"role": "user", "content": query}]}

    # Invoke the agent
    response = agent.invoke(state)

    # Extract AI messages correctly
    messages = response.get("messages", [])

    if messages:
        ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
        
        # Debugging Output
        return ai_messages[-1]

        # If the AI message is in JSON format, parse it
        if "<tavily_search_results_json>" in ai_messages[-1]:
            # --- FIX: Clean the string before parsing ---
            search_data = (
                ai_messages[-1]
                .replace("<tavily_search_results_json>", "")
                .replace("</tavily_search_results_json>", "")
                .strip("`")
                .strip()
            )

            try:
                search_query = json.loads(search_data).get("query")  # Safely extract query
                print(f"Performing search for: {search_query}")
                # Use the search tool correctly
                search_results = search_tool.invoke(search_query)
                print("Search Results:", search_results)
            except json.JSONDecodeError as e:
                print("Error parsing search JSON:", e)
                print("Raw AI response:", search_data)  # Debugging output
        else:
            print("No Tavily search JSON found in AI response.")
    else:
        print("No AI messages found in response.")
