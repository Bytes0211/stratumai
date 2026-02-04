"""OpenRouter chat interface for StratumAI.

Provides convenient functions for OpenRouter chat completions with sensible defaults.
OpenRouter provides unified access to models from multiple providers.

Default Model: meta-llama/llama-3.3-70b-instruct:free
Environment Variable: OPENROUTER_API_KEY
"""

import asyncio
from typing import AsyncIterator, Optional, Union

from stratumai import LLMClient
from stratumai.models import ChatResponse, Message

# Default configuration
DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = None

# Module-level client (lazy initialization)
_client: Optional[LLMClient] = None


def _get_client() -> LLMClient:
    """Get or create the module-level client."""
    global _client
    if _client is None:
        _client = LLMClient(provider="openrouter")
    return _client


async def chat(
    prompt: Union[str, list[Message]],
    *,
    model: str = DEFAULT_MODEL,
    system: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: Optional[int] = DEFAULT_MAX_TOKENS,
    stream: bool = False,
    **kwargs,
) -> Union[ChatResponse, AsyncIterator[ChatResponse]]:
    """
    Send a chat completion request to OpenRouter.

    Args:
        prompt: User message string or list of Message objects.
        model: Model name. Default: meta-llama/llama-3.3-70b-instruct:free
        system: Optional system prompt (ignored if prompt is list of Messages).
        temperature: Sampling temperature (0.0-2.0). Default: 0.7
        max_tokens: Maximum tokens to generate. Default: None (model default)
        stream: Whether to stream the response. Default: False
        **kwargs: Additional parameters passed to the API.

    Returns:
        ChatResponse object, or AsyncIterator[ChatResponse] if streaming.

    Example:
        >>> from stratumai.chat import openrouter
        >>> response = openrouter.chat("What is Python?")
        >>> print(response.content)

        # Use a different model
        >>> response = openrouter.chat(
        ...     "Explain AI",
        ...     model="anthropic/claude-3-5-sonnet"
        ... )
    """
    client = _get_client()

    # Build messages list
    if isinstance(prompt, str):
        messages = []
        if system:
            messages.append(Message(role="system", content=system))
        messages.append(Message(role="user", content=prompt))
    else:
        messages = prompt

    return await client.chat(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
        **kwargs,
    )


async def chat_stream(
    prompt: Union[str, list[Message]],
    *,
    model: str = DEFAULT_MODEL,
    system: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: Optional[int] = DEFAULT_MAX_TOKENS,
    **kwargs,
) -> AsyncIterator[ChatResponse]:
    """
    Send a streaming chat completion request to OpenRouter.

    Args:
        prompt: User message string or list of Message objects.
        model: Model name. Default: meta-llama/llama-3.3-70b-instruct:free
        system: Optional system prompt (ignored if prompt is list of Messages).
        temperature: Sampling temperature (0.0-2.0). Default: 0.7
        max_tokens: Maximum tokens to generate. Default: None (model default)
        **kwargs: Additional parameters passed to the API.

    Yields:
        ChatResponse chunks.

    Example:
        >>> from stratumai.chat import openrouter
        >>> for chunk in openrouter.chat_stream("Tell me a story"):
        ...     print(chunk.content, end="", flush=True)
    """
    return await chat(
        prompt,
        model=model,
        system=system,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
        **kwargs,
    )


def chat_sync(
    prompt,
    *,
    model=DEFAULT_MODEL,
    system=None,
    temperature=DEFAULT_TEMPERATURE,
    max_tokens=DEFAULT_MAX_TOKENS,
    **kwargs,
):
    """Synchronous wrapper for chat()."""
    return asyncio.run(chat(
        prompt,
        model=model,
        system=system,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
        **kwargs,
    ))
