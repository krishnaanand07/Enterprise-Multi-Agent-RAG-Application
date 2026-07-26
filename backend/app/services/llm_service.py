"""
LLM Service — Unified interface for language model providers.

Supports Google Gemini and OpenAI GPT models.
The provider is selected via the LLM_PROVIDER environment variable.

Usage:
    from app.services.llm_service import llm_service

    response = await llm_service.generate("Explain quantum computing.")
"""

from typing import AsyncGenerator, Optional
from loguru import logger

from app.config.settings import settings


class LLMService:
    """
    Unified LLM service that abstracts provider differences.
    """

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self._gemini_model = None
        self._openai_client = None
        self._nvidia_client = None

    def _init_gemini(self):
        """Lazily initialize Google Gemini client."""
        if self._gemini_model is None:
            import google.generativeai as genai

            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self._gemini_model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                },
            )
            logger.info(f"Initialized Gemini model: {settings.GEMINI_MODEL}")
        return self._gemini_model

    def _init_openai(self):
        """Lazily initialize OpenAI client."""
        if self._openai_client is None:
            from openai import AsyncOpenAI

            self._openai_client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY
            )
            logger.info(f"Initialized OpenAI model: {settings.OPENAI_MODEL}")
        return self._openai_client

    def _init_nvidia(self):
        """Lazily initialize NVIDIA client (using OpenAI compatible API)."""
        if self._nvidia_client is None:
            from openai import AsyncOpenAI

            self._nvidia_client = AsyncOpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=settings.NVIDIA_API_KEY
            )
            logger.info(f"Initialized NVIDIA model: {settings.NVIDIA_MODEL}")
        return self._nvidia_client

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """Generate a response from the LLM."""
        if self.provider == "gemini":
            return await self._generate_gemini(
                prompt, system_prompt, temperature, max_tokens
            )
        elif self.provider == "openai":
            return await self._generate_openai(
                prompt, system_prompt, temperature, max_tokens
            )
        elif self.provider == "nvidia":
            return await self._generate_nvidia(
                prompt, system_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    async def _generate_gemini(
        self, prompt, system_prompt, temperature, max_tokens
    ) -> str:
        """Generate response using Google Gemini."""
        model = self._init_gemini()
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = await model.generate_content_async(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )
        return response.text

    async def _generate_openai(
        self, prompt, system_prompt, temperature, max_tokens
    ) -> str:
        """Generate response using OpenAI GPT."""
        client = self._init_openai()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def _generate_nvidia(
        self, prompt, system_prompt, temperature, max_tokens
    ) -> str:
        """Generate response using NVIDIA NIM."""
        client = self._init_nvidia()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream a response from the LLM token by token."""
        if self.provider == "gemini":
            async for chunk in self._stream_gemini(prompt, system_prompt):
                yield chunk
        elif self.provider == "openai":
            async for chunk in self._stream_openai(prompt, system_prompt):
                yield chunk
        elif self.provider == "nvidia":
            async for chunk in self._stream_nvidia(prompt, system_prompt):
                yield chunk

    async def _stream_gemini(
        self, prompt, system_prompt
    ) -> AsyncGenerator[str, None]:
        """Stream response from Gemini."""
        model = self._init_gemini()
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = await model.generate_content_async(
            full_prompt, stream=True,
        )
        async for chunk in response:
            if chunk.text:
                yield chunk.text

    async def _stream_openai(
        self, prompt, system_prompt
    ) -> AsyncGenerator[str, None]:
        """Stream response from OpenAI."""
        client = self._init_openai()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def _stream_nvidia(
        self, prompt, system_prompt
    ) -> AsyncGenerator[str, None]:
        """Stream response from NVIDIA."""
        client = self._init_nvidia()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


# Singleton instance
llm_service = LLMService()
