# StratumAI - Unified Intelligence Across Every Model Layer

**Status:** Phase 7.2 Complete ✅ | 8 Providers Operational | Intelligent File Extraction

## Why This Project Matters

StratumAI is a production-ready Python module that provides a unified, abstracted interface for accessing multiple frontier LLM providers (OpenAI, Anthropic, Google, DeepSeek, Groq, Grok, OpenRouter, Ollama) through a consistent API. It eliminates vendor lock-in, simplifies multi-model development, and enables intelligent routing between providers.

## Key Skills Demonstrated

- **API Abstraction & Design Patterns**: Strategy pattern, factory pattern, provider abstraction
- **Multi-Provider Integration**: 8 LLM providers with unified interface
- **Production Engineering**: Error handling, retry logic, cost tracking, budget management
- **Python Best Practices**: Type hints, dataclasses, abstract base classes, decorators
- **Testing & Quality**: Unit tests, integration tests, 80%+ coverage target
- **DevOps & Packaging**: PyPI package preparation, uv/pip dependency management

## Project Overview

StratumAI is a multi-provider LLM abstraction module that allows developers/users to switch between AI models from different providers without changing their code. The module provides automatic retry with fallback, cost tracking, intelligent routing, and advanced features like streaming, caching, and budget management.

### What This Project Delivers

**Core Platform:**

- **Unified Interface**: Single API for all LLM providers (OpenAI, Anthropic, Google, DeepSeek, Groq, Grok, OpenRouter, Ollama)
- **Zero-Lock-In**: Switch models without code changes
- **Cost Tracking**: Automatic token usage and cost calculation per request
- **Automatic Retry**: Exponential backoff with fallback model support
- **Intelligent Router**: Select optimal model based on cost, quality, or hybrid strategies
- **Advanced Features**: Streaming, caching, logging decorators, budget limits

### Key Technical Achievements

- ✅ Project initialized with comprehensive technical design (1,232 lines)
- ✅ 7-week implementation roadmap completed
- ✅ 8 provider implementations complete
- ✅ Streaming support for all providers
- ✅ Cost tracking accurate to $0.0001
- ✅ Production-ready error handling and retry logic
- ✅ Web GUI with FastAPI and interactive interface
- ✅ Intelligent routing with complexity analysis
- ✅ Rich/Typer CLI for terminal usage (Phase 5 Complete)

## Architecture Overview

**Design Principles:**
- **Abstraction First**: Hide provider-specific differences behind unified interface
- **Strategy Pattern**: Each provider implements common BaseProvider interface
- **Configuration-Driven**: Model catalogs, cost tables, capability matrices externalized

**Core Components:**
1. **BaseProvider**: Abstract interface that all providers implement
2. **LLMClient**: Unified client with provider detection and routing
3. **Provider Implementations**: 8 providers (OpenAI, Anthropic, Google, DeepSeek, Groq, Grok, OpenRouter, Ollama)
4. **Cost Tracker**: Track usage and enforce budget limits
5. **Router**: Intelligent model selection based on complexity analysis
6. **Decorators**: Logging, caching, retry utilities

**Request Flow:**
```
User → LLMClient → Provider Detection → Provider Implementation → LLM API
                                      ↓
                                Cost Tracking → Budget Check
```

## Technology Stack

### Core Technologies
- **Python 3.10+**: Core language with type hints
- **OpenAI SDK**: For OpenAI and OpenAI-compatible providers
- **Anthropic SDK**: For Claude models
- **Google Generative AI SDK**: For Gemini models

### Development
- **Languages:** Python 3.10+
- **Package Manager:** uv (alternative: pip)
- **Testing:** pytest, pytest-cov, pytest-mock
- **Code Quality:** black (formatting), ruff (linting), mypy (type checking)
- **Version Control:** Git with conventional commits
- **Documentation:** Markdown, docstrings

## Setup Instructions

### Prerequisites
- Python 3.12+ with venv support
- uv (recommended) or pip for package management

### Initial Setup

1. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. **Configure API keys:**
   ```bash
   # Create .env file with your API keys
   cp .env.example .env
   # Edit .env and add your keys
   ```

3. **Run the CLI:**
   ```bash
   # Install CLI dependencies
   pip install typer[all]
   
   # Use the CLI
   python -m cli.stratumai_cli chat -p openai -m gpt-4o-mini -t "Hello"
   
   # Or run the Web GUI (optional)
   uv run uvicorn api.main:app --reload
   ```

## Project Structure

```txt
stratumai/
├── README.md
├── WARP.md
├── requirements.txt
├── .venv/
├── docs/
│   ├── project-status.md              # 6-week timeline with detailed phases
│   └── stratumai-technical-approach.md # Comprehensive technical design (1,232 lines)
├── cli/
│   └── stratumai_cli.py               # Rich/Typer CLI interface
├── api/                                # Optional FastAPI web interface
│   ├── main.py                         # FastAPI application
│   └── static/                         # Web UI files
├── examples/
│   ├── router_example.py               # Router usage examples
│   └── caching_examples.py             # Caching decorator examples
└─ llm_abstraction/                    # Main package
    ├── __init__.py
    ├── client.py                       # Unified LLMClient
    ├── models.py                       # Data models (Message, ChatRequest, ChatResponse)
    ├── config.py                       # Model catalogs and cost tables
    ├── exceptions.py                   # Custom exceptions
    ├── cost_tracker.py                 # Cost tracking module
    ├── retry.py                        # Retry logic with fallbacks
    ├── caching.py                      # Response caching
    ├── router.py                       # Intelligent routing
    ├── chunking.py                     # Smart content chunking
    ├── summarization.py                # Progressive summarization
    ├── utils/                          # Utilities (Phase 7.1)
    │   ├── token_counter.py            # Token estimation
    │   └── file_analyzer.py            # File type detection
    └── providers/
        ├── base.py                     # BaseProvider abstract class
        ├── openai.py                   # OpenAI implementation
        ├── anthropic.py                # Anthropic implementation
        ├── google.py                   # Google Gemini implementation
        ├── deepseek.py                 # DeepSeek implementation
        ├── groq.py                     # Groq implementation
        ├── grok.py                     # Grok (X.AI) implementation
        ├── openrouter.py               # OpenRouter implementation
        └── ollama.py                   # Ollama local models
```

## Key Features

### Core Features
- **Unified Interface**: Single API for 8 LLM providers
- **Provider Abstraction**: BaseProvider interface with consistent methods
- **Automatic Provider Detection**: Infer provider from model name
- **Cost Calculation**: Per-request token usage and cost tracking
- **Error Handling**: Custom exception hierarchy for different failure modes

### Advanced Features
- **Streaming Support**: Iterator-based streaming for all providers
- **Cost Tracker**: Call history, grouping by provider/model, budget enforcement
- **Retry Logic**: Exponential backoff with configurable fallback models
- **Caching Decorator**: Cache responses with configurable TTL
- **Logging Decorator**: Comprehensive logging of all LLM calls
- **Budget Management**: Set limits and receive alerts

### Router Features
- **Complexity Analysis**: Analyze prompt to determine appropriate model tier
- **Routing Strategies**: Cost-optimized, quality-focused, latency-focused, or hybrid
- **Model Metadata**: Context windows, capabilities, performance characteristics
- **Performance Benchmarks**: Latency, cost, and quality metrics

### CLI Features ✅
- **Rich/Typer Interface**: Beautiful terminal UI with colors, tables, and spinners
- **Core Commands**: chat, models, providers, route, interactive
- **Numbered Selection**: Choose provider/model by number instead of typing names
- **Reasoning Model Labels**: Visual indicators for reasoning models (o1, o3-mini, deepseek-reasoner)
- **Fixed Temperature Handling**: Automatic temperature setting for reasoning models
- **Enhanced Metadata Display**: Provider, Model, Context Window, Token Breakdown, Cost
- **Token Breakdown**: Separate display of input tokens, output tokens, and total tokens (In: X | Out: Y | Total: Z)
- **Spinner Feedback**: Animated "Thinking..." indicator while waiting for responses
- **Streaming Output**: Real-time LLM responses with no flicker
- **Interactive Mode**: Conversation loop with history, context display, and special commands
  - `/file <path>` - Load and send file immediately
  - `/attach <path>` - Stage file for next message
  - `/clear` - Clear staged attachments
  - `/provider` - Switch provider and model mid-conversation (preserves history)
  - `/help` - Display available commands and session info
  - `exit, quit, q` - Exit interactive mode
- **File Attachments**: Upload files via `--file` flag or in-conversation commands
- **File Size Limits**: 5 MB max with warnings for files >500 KB
- **Conversation Persistence**: History maintained when switching providers/models
- **Markdown Export**: Save responses as markdown files with metadata
- **Router Integration**: Auto-select best model from CLI
- **Environment Variables**: Native support for STRATUMAI_PROVIDER, STRATUMAI_MODEL

### Large File Handling Features
- **Token Counting**: Provider-specific token estimation with tiktoken for OpenAI
- **File Analysis**: Automatic file type detection (CSV, JSON, Python, logs, etc.)
- **Smart Chunking**: Split large files at paragraph/sentence boundaries
- **Progressive Summarization**: Multi-chunk summarization with cheaper models
- **CLI Integration**: `--chunked` and `--chunk-size` flags for chat command
- **Token Warnings**: Alert when approaching model context limits (>80%)
- **Reduction Stats**: Display token reduction percentage after summarization

## Project Status

**Current Phase:** Phase 7.2 - Intelligent Extraction ✅ COMPLETE

**Progress:** Phases 1-6 Complete + Phase 7.1-7.2 Complete

**Completed Phases:**
- ✅ **Phase 1:** Core Implementation (5/5 tasks)
  - BaseProvider abstract class
  - OpenAI provider with cost tracking
  - Unified LLMClient
  - Custom exception hierarchy
  - 32 unit tests passing

- ✅ **Phase 2:** Provider Expansion (9/9 tasks)
  - Anthropic provider with Messages API
  - OpenAICompatibleProvider base class
  - Google, DeepSeek, Groq, Grok, Ollama, OpenRouter providers
  - 77 total tests passing
  - All 8 providers operational

- ✅ **Phase 3:** Advanced Features (6/6 tasks)
  - Cost tracking module with analytics
  - Budget limits and alerts
  - Retry logic with exponential backoff
  - Fallback model/provider support
  - Streaming support (all providers)
  - Cache statistics tracking

- ✅ **Phase 3.5:** Web GUI (4/4 tasks)
  - FastAPI REST API
  - WebSocket streaming
  - Interactive web interface
  - Real-time cost tracking dashboard

- ✅ **Phase 4:** Router and Optimization (5/5 tasks)
  - Router with intelligent model selection
  - Complexity analysis algorithm
  - Cost/quality/latency/hybrid strategies
  - 33 router unit tests passing

- ✅ **Phase 5:** CLI Interface (4/4 tasks)
  - Typer CLI framework with Rich formatting
  - Core commands (chat, models, providers, route, interactive)
  - Numbered selection with reasoning labels
  - Enhanced metadata display and user experience
  - Markdown export functionality
  - Loop functionality for multiple queries

- ✅ **Phase 6:** Production Readiness (6/6 tasks)
  - Complete API documentation (API-REFERENCE.md, GETTING-STARTED.md)
  - 6 example applications (chatbot, code reviewer, document summarizer, performance benchmark, router examples, caching examples)
  - Performance optimization (<200ms cold start, <20MB memory)
  - Prompt caching system (response cache + provider caching)
  - CLI cache visibility and file input enhancements
  - PyPI package preparation (setup.py, pyproject.toml, MANIFEST.in)

- ✅ **Phase 7.1:** Large File Handling - Token Estimation & Chunking (5/5 tasks)
  - Token counting utility (tiktoken for OpenAI)
  - File type analysis and warnings
  - Smart chunking at natural boundaries
  - Progressive summarization with cheaper models
  - CLI integration (--chunked, --chunk-size flags)
  - 19 unit tests passing

- ✅ **Phase 7.2:** Intelligent Extraction (4/4 tasks)
  - CSV schema extraction (26-99% token reduction) - 197 lines
  - JSON schema extraction (78-95% token reduction) - 219 lines
  - Log error extraction (90% token reduction) - 267 lines
  - Code structure extraction with AST (33-80% reduction) - 327 lines
  - `analyze` CLI command for all file types
  - pandas dependency for CSV processing
  - 35 unit tests passing (100%)

**Next Steps:**
- 📝 Phase 7.3: Model Auto-Selection
- 📝 Phase 7.4: Enhanced Caching UI
- 📝 Phase 7.5: RAG/Vector DB Integration (ChromaDB)

## Usage Examples

### CLI Usage (Phase 5 - Complete ✅)
```bash
# Quick start with interactive mode
./start_app.sh

# Simple chat with command-line args
python -m cli.stratumai_cli chat "What is AI?" --provider openai --model gpt-4o-mini

# Interactive prompts (numbered selection)
python -m cli.stratumai_cli chat
# Prompts for:
# 1. Provider (1-8)
# 2. Model (numbered list with reasoning labels)
# 3. Temperature (auto-set for reasoning models)
# 4. Your message
# Then shows: Provider | Model | Context | In: X | Out: Y | Total: Z | Cost

# Streaming mode
python -m cli.stratumai_cli chat "Write a poem" --provider openai --model gpt-4o-mini --stream

# Auto-route to best model
python -m cli.stratumai_cli route "Explain quantum computing" --strategy hybrid

# Interactive conversation mode with special commands
python -m cli.stratumai_cli interactive --provider anthropic --model claude-sonnet-4-5-20250929
# Within interactive mode:
#   /file <path>     - Load and send file
#   /attach <path>   - Stage file for next message
#   /clear           - Clear staged files
#   /provider        - Switch provider/model (history preserved)
#   /help            - Show commands and session info
#   exit, quit, q    - Exit

# Interactive mode with initial file context
python -m cli.stratumai_cli interactive --file document.txt

# Chat with file attachment
python -m cli.stratumai_cli chat --file report.pdf --provider openai --model gpt-4o

# Chat with large file using chunking and summarization
python -m cli.stratumai_cli chat --file large_document.txt --chunked --provider openai --model gpt-4o-mini

# Chat with custom chunk size
python -m cli.stratumai_cli chat --file data.csv --chunked --chunk-size 100000 --provider openai --model gpt-4o-mini

# List all models
python -m cli.stratumai_cli models

# List models for specific provider
python -m cli.stratumai_cli models --provider openai

# List all providers
python -m cli.stratumai_cli providers

# With environment variables
export STRATUMAI_PROVIDER=anthropic
export STRATUMAI_MODEL=claude-sonnet-4-5-20250929
python -m cli.stratumai_cli chat "Hello"
```

### Python Library Usage
```python
from llm_abstraction import LLMClient

# Initialize client (reads API keys from environment)
client = LLMClient()

# Simple chat completion
response = client.chat(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    temperature=0.7
)

print(response.content)
print(f"Cost: ${response.usage.cost_usd:.4f}")
```

### Switching Models (No Code Changes)
```python
# Switch to Anthropic - same interface!
response = client.chat(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Switch to Google - still same interface!
response = client.chat(
    model="gemini-2.5-flash-lite",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Streaming Responses
```python
from llm_abstraction import LLMClient, ChatRequest

client = LLMClient()
request = ChatRequest(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Write a poem"}]
)

for chunk in client.chat_completion_stream(request):
    print(chunk.content, end="", flush=True)
```

### With Cost Tracking
```python
from llm_abstraction import LLMClient, CostTracker

client = LLMClient()
tracker = CostTracker(budget_limit=10.0)

for i in range(10):
    response = client.chat(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": f"Question {i}"}]
    )
    tracker.record_call(response.model, response.provider, response.usage)

print(tracker.get_summary())
```

## Examples

The `examples/` directory contains 6 comprehensive real-world examples:

1. **caching_examples.py** - Response caching and cost optimization with TTL
2. **chatbot.py** - Interactive chatbot with conversation history and persistence
3. **code_reviewer.py** - Code review with multi-model comparison
4. **document_summarizer.py** - Batch document summarization with progress tracking
5. **performance_benchmark.py** - Performance benchmarking tool for latency/cost/memory
6. **router_example.py** - Intelligent model routing demonstrations

All examples are fully working and verified (✅ Feb 3, 2026):
```bash
python examples/router_example.py
python examples/chatbot.py --model gpt-4o-mini
python examples/code_reviewer.py mycode.py --compare
python examples/document_summarizer.py docs/*.txt
python examples/performance_benchmark.py --requests 5
python examples/caching_examples.py
```

## Documentation

### Core Documentation
- **README.md** - This file (project overview and setup)
- **WARP.md** - Development environment guidance and project status
- **docs/stratumai-technical-approach.md** - Comprehensive technical design (1,232 lines)
- **docs/project-status.md** - Detailed implementation timeline

## Testing

The project has comprehensive test coverage:
- **Unit Tests**: 77+ tests for core functionality
- **Integration Tests**: Provider-specific tests for all 8 providers
- **Router Tests**: 33 tests for intelligent model selection
- **Phase 7.1 Tests**: 19 tests for token counting, chunking, and summarization

Run tests with:
```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_*.py    # Specific test file
```

## License

Internal project - All rights reserved

## Contact

Project Owner: scotton
