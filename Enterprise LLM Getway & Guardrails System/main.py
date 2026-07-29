from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from services import process_chat_request

app = FastAPI(
    title="Enterprise LLM Gateway",
    description="Modular Production-Ready LLM Gateway with Observability, Caching & Guardrails",
    version="2.0.0"
)
"""
Prometheus Instrumentation
"""
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

class ChatRequest(BaseModel):
    user_id: str
    prompt: str
    model: str = "llama-3.3-70b-versatile"

class ChatResponse(BaseModel):
    response: str
    model_used: str
    trace_id: str
    cached: bool = False
    blocked: bool = False

@app.post("/v1/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    result = await process_chat_request(
        user_id=request.user_id,
        prompt=request.prompt,
        model=request.model
    )
    return ChatResponse(**result)