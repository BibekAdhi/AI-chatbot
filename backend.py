#STEP1: SETUP PYDANTIC MODEL (SCHEMA VALIDATION)
from pydantic import BaseModel
from typing import List


class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool





#STEP2: SETUP AI AGENT FROM FRONTEND REQUEST
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODEL_NAMES=["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-40-mini"]

app = FastAPI(title="Langgraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    if request.moodel_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider
    
    #Create AI Agent and get response from it!
    response=get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response

#STEP3: RUN APP AND EXPLORE SWAGGER UI DOCS