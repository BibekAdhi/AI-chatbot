#SETUP API KEYS FOR groq, OpenAI, and Tavily

import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


#SETUP LLM and TOOLS

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")


search_tool=TavilySearchResults(max_results=2)


#SETUP AI AGENT WITH SEARCH TOOL FUNCTIONALITY
from langgraph.prebuilt import create_react_agent



system_prompt = "Act as an AI chatbot who is smart and friendly"

agent = create_react_agent(
    model=groq_llm,
    tools=[search_tool],
    prompt=system_prompt 
)



#query = "Tell me about the trends in crypto markets"
#state = {"messages":query}
#response = agent.invoke(state)
#print(response)
query = "Tell me about the trends in crypto markets"
state = {"messages": [{"role": "user", "content": query}]}
response = agent.invoke(state)
print(response)

