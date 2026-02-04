![StratumAI](stratum_logo.png)

# StratumAI — Unified Multi‑Provider LLM Interface

**Status:** Phase 7.8 Complete  
**Providers:** 9 Operational  
**Features:** Routing • RAG • Caching • Streaming • CLI • Web UI • Builder Pattern

StratumAI is a production‑ready Python framework that provides a unified interface for 9+ LLM providers, including OpenAI, Anthropic, Google, DeepSeek, Groq, Grok, OpenRouter, Ollama, and AWS Bedrock. It eliminates vendor lock‑in, simplifies multi‑model development, and enables intelligent routing, cost tracking, caching, streaming, and RAG workflows.

---

## Features

### Core

- Unified API for 9+ LLM providers
- Async-first architecture with sync wrappers
- Automatic provider detection
- Cost tracking and budget enforcement
- Latency tracking on all responses
- Retry logic with fallback models
- Streaming support for all providers
- Response caching + provider prompt caching
- Intelligent routing (cost, quality, latency, hybrid)
- Capability filtering (vision, tools, reasoning)
- Model metadata and context window awareness
- **Builder pattern** for fluent configuration

### Advanced

- Large‑file handling with chunking and progressive summarization
- File extraction (CSV schema, JSON schema, logs, code structure)
- Auto model selection for extraction tasks
- RAG pipeline with embeddings + vector DB (ChromaDB)
- Semantic search and citation tracking
- Rich/Typer CLI with interactive mode
- Optional FastAPI web interface

---

## Installation

```bash
git clone https://github.com/Bytes0211/stratumai.git
cd stratumai
pip install -e .
```

Or using `uv`:

```bash
uv sync
```

---

## Configuration

```bash
cp .env.example .env
# Add your API keys
```

Check configured providers:

```bash
stratumai check-keys
```

---

## Quick Start

### CLI Usage

```bash
stratumai chat -p openai -m gpt-4o-mini -t "Hello"
stratumai route "Explain relativity" --strategy hybrid
stratumai interactive
stratumai cache-stats
```

### Python Example (LLMClient)

```python
from stratumai import LLMClient
from stratumai.models import Message, ChatRequest

client = LLMClient()
request = ChatRequest(
    model="gpt-4o-mini",
    messages=[Message(role="user", content="Explain quantum computing")]
)

# Async (recommended)
response = await client.chat_completion(request)

# Sync wrapper for scripts/CLI
response = client.chat_completion_sync(request)

print(response.content)
print(f"Cost: ${response.usage.cost_usd:.6f}")
print(f"Latency: {response.latency_ms:.0f}ms")
```

### Python Example (Chat Package - Simplified)

```python
from stratumai.chat import anthropic, openai

# Quick usage - model is always required
response = await anthropic.chat("Hello!", model="claude-sonnet-4-5")
print(response.content)

# With options
response = await openai.chat(
    "Explain quantum computing",
    model="gpt-4o-mini",
    system="Be concise",
    temperature=0.5
)
```

### Builder Pattern (Fluent Configuration)

```python
from stratumai.chat import anthropic

# Configure once, use multiple times
client = (
    anthropic
    .with_model("claude-sonnet-4-5")
    .with_system("You are a helpful assistant")
    .with_temperature(0.7)
)

# All subsequent calls use the configured settings
response = await client.chat("Hello!")
response = await client.chat("Tell me more")

# Stream with builder
async for chunk in client.chat_stream("Write a story"):
    print(chunk.content, end="", flush=True)
```

---

## Routing

- **Cost**: choose cheapest model
- **Quality**: choose highest‑quality model
- **Latency**: choose fastest model
- **Hybrid (default)**: dynamic weighting based on complexity

---

## RAG

- Embeddings (OpenAI)
- ChromaDB vector storage
- Semantic search
- Document indexing
- Retrieval‑augmented generation
- Citation tracking

---

## Project Structure

```
stratumai/
├── llm_abstraction/      # Core package
│   ├── providers/        # Provider implementations (9 providers)
│   ├── router.py         # Intelligent routing
│   ├── models.py         # Data models
│   └── utils/            # Utilities (token counting, extraction)
├── chat/                 # Simplified chat modules with builder pattern
│   ├── builder.py        # ChatBuilder class
│   └── stratumai_*.py    # Provider-specific modules
├── cli/                  # Typer CLI
├── api/                  # Optional FastAPI server
├── examples/             # Usage examples
└── docs/                 # Technical documentation
```

---

## Testing

```bash
pytest           # Run all tests
pytest -v        # Verbose output
```

**Test Coverage:** 300+ tests across all modules

---

## License

Internal project — All rights reserved.

