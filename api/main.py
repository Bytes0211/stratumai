"""FastAPI application for StratumAI."""

import json
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from llm_abstraction import LLMClient, ChatRequest, Message, ProviderType
from llm_abstraction.cost_tracker import CostTracker
from llm_abstraction.config import MODEL_CATALOG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="StratumAI API",
    description="Unified API for multiple LLM providers",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global cost tracker
cost_tracker = CostTracker()

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Request/Response models
class ChatCompletionRequest(BaseModel):
    """Chat completion request model."""
    provider: str
    model: str
    messages: List[dict]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False


class ChatCompletionResponse(BaseModel):
    """Chat completion response model."""
    id: str
    provider: str
    model: str
    content: str
    finish_reason: str
    usage: dict
    cost_usd: float


class ProviderInfo(BaseModel):
    """Provider information model."""
    name: str
    models: List[str]


@app.get("/")
async def root():
    """Serve the frontend interface."""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "name": "StratumAI API",
        "version": "0.1.0",
        "message": "Frontend not found. API endpoints available at /docs"
    }


@app.get("/api/providers", response_model=List[str])
async def list_providers():
    """List all available providers."""
    return [
        "openai",
        "anthropic",
        "google",
        "deepseek",
        "groq",
        "grok",
        "ollama",
        "openrouter",
    ]


@app.get("/api/models/{provider}", response_model=List[str])
async def list_models(provider: str):
    """List models for a specific provider."""
    if provider not in MODEL_CATALOG:
        raise HTTPException(status_code=404, detail=f"Provider '{provider}' not found")
    
    return list(MODEL_CATALOG[provider].keys())


@app.get("/api/provider-info", response_model=List[ProviderInfo])
async def get_provider_info():
    """Get information about all providers and their models."""
    providers = []
    for provider_name, models in MODEL_CATALOG.items():
        providers.append(ProviderInfo(
            name=provider_name,
            models=list(models.keys())
        ))
    return providers


@app.post("/api/chat", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest):
    """
    Execute a chat completion request.
    
    Args:
        request: Chat completion request
        
    Returns:
        Chat completion response with cost tracking
    """
    try:
        # Convert messages to Message objects
        messages = [
            Message(role=msg["role"], content=msg["content"])
            for msg in request.messages
        ]
        
        # Create chat request
        chat_request = ChatRequest(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        # Initialize client and make request
        client = LLMClient(provider=request.provider)
        response = client.chat(chat_request)
        
        # Track cost
        cost_tracker.add_entry(
            provider=response.provider,
            model=response.model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            cost_usd=response.usage.cost_usd,
            request_id=response.id,
            cached_tokens=response.usage.cached_tokens,
            cache_creation_tokens=response.usage.cache_creation_tokens,
            cache_read_tokens=response.usage.cache_read_tokens,
        )
        
        return ChatCompletionResponse(
            id=response.id,
            provider=response.provider,
            model=response.model,
            content=response.content,
            finish_reason=response.finish_reason,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            cost_usd=response.usage.cost_usd,
        )
    except Exception as e:
        logger.error(f"Chat completion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/api/chat/stream")
async def chat_stream(websocket: WebSocket):
    """
    WebSocket endpoint for streaming chat completions.
    
    Protocol:
        Client sends JSON: {"provider": "openai", "model": "gpt-4", "messages": [...]}
        Server streams JSON chunks: {"content": "...", "done": false}
        Final message: {"content": "", "done": true, "usage": {...}}
    """
    await websocket.accept()
    
    try:
        # Receive request
        data = await websocket.receive_text()
        request_data = json.loads(data)
        
        provider = request_data.get("provider")
        model = request_data.get("model")
        messages_data = request_data.get("messages", [])
        temperature = request_data.get("temperature", 0.7)
        max_tokens = request_data.get("max_tokens")
        
        # Convert messages
        messages = [
            Message(role=msg["role"], content=msg["content"])
            for msg in messages_data
        ]
        
        # Create request
        chat_request = ChatRequest(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        # Initialize client and stream
        client = LLMClient(provider=provider)
        
        full_content = ""
        for chunk in client.chat_stream(chat_request):
            full_content += chunk.content
            await websocket.send_json({
                "content": chunk.content,
                "done": False,
            })
        
        # Send final message
        await websocket.send_json({
            "content": "",
            "done": True,
            "full_content": full_content,
        })
        
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.send_json({
            "error": str(e),
            "done": True,
        })
    finally:
        await websocket.close()


@app.get("/api/cost")
async def get_cost_summary():
    """Get cost tracking summary."""
    return cost_tracker.get_summary()


@app.post("/api/cost/reset")
async def reset_cost_tracker():
    """Reset cost tracker."""
    cost_tracker.reset()
    return {"message": "Cost tracker reset successfully"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
