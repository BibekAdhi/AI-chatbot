from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from ai_agent import get_response_from_ai_agent

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    try:
        response_text = get_response_from_ai_agent(
            llm_id=data.get("model_name"),
            query=data.get("messages")[0],
            allow_search=data.get("allow_search", False),
            system_prompt=data.get("system_prompt", ""),
            provider=data.get("model_provider", "Groq")
        )
        return JSONResponse(content={"response": response_text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    # Run with reload=True for dev convenience
    uvicorn.run("backend:app", host="127.0.0.1", port=9999, reload=True)
