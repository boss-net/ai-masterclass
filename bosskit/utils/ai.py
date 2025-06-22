import json
import logging
import os
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

import openai  # type: ignore

from .errors import APIError  # type: ignore
from .logging_utils import setup_logger


class AIProcessor:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        logger: Optional[logging.Logger] = None,
    ):
        """Initialize the AI processor.

        Args:
            api_key: OpenAI API key
            model: Model name
            temperature: Temperature setting
            max_tokens: Maximum tokens
            logger: Logger instance
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = logger or setup_logger("bosskit.ai")

        if not self.api_key:
            raise ValueError("API key is required")

        openai.api_key = self.api_key

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        functions: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a chat completion.

        Args:
            messages: Chat messages
            functions: Available functions
            temperature: Temperature override
            max_tokens: Token limit override

        Returns:
            Completion response

        Raises:
            APIError: If request fails
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                functions=functions,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            return response
        except Exception as e:
            raise APIError(f"Failed to create chat completion: {str(e)}") from e

    async def stream_chat_completion(
        self,
        messages: List[Dict[str, str]],
        functions: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream chat completion.

        Args:
            messages: Chat messages
            functions: Available functions
            temperature: Temperature override
            max_tokens: Token limit override

        Yields:
            Completion chunks

        Raises:
            APIError: If request fails
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                functions=functions,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=True,
            )

            async for chunk in response:
                yield chunk
        except Exception as e:
            raise APIError(f"Failed to stream chat completion: {str(e)}") from e

    async def function_calling(
        self,
        messages: List[Dict[str, str]],
        functions: List[Dict[str, Any]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Execute function calling.

        Args:
            messages: Chat messages
            functions: Available functions
            temperature: Temperature override
            max_tokens: Token limit override

        Returns:
            Function call response

        Raises:
            APIError: If request fails
        """
        try:
            response = await self.chat_completion(
                messages=messages, functions=functions, temperature=temperature, max_tokens=max_tokens
            )

            if not response.choices[0].message.function_call:
                raise ValueError("No function call in response")

            return json.loads(response.choices[0].message.function_call.arguments)
        except Exception as e:
            raise APIError(f"Failed to execute function calling: {str(e)}") from e

    async def embeddings(self, text: Union[str, List[str]], model: Optional[str] = None) -> List[List[float]]:
        """Generate embeddings.

        Args:
            text: Input text or list of texts
            model: Embedding model

        Returns:
            List of embeddings

        Raises:
            APIError: If request fails
        """
        try:
            response = await openai.Embedding.acreate(input=text, model=model or "text-embedding-ada-002")

            if isinstance(text, str):
                return [response.data[0].embedding]

            return [d.embedding for d in response.data]
        except Exception as e:
            raise APIError(f"Failed to generate embeddings: {str(e)}") from e

    async def image_generation(
        self, prompt: str, n: int = 1, size: str = "1024x1024", response_format: str = "url"
    ) -> List[Union[str, bytes]]:
        """Generate images.

        Args:
            prompt: Image prompt
            n: Number of images
            size: Image size
            response_format: Response format ('url' or 'b64_json')

        Returns:
            List of image URLs or base64 data

        Raises:
            APIError: If request fails
        """
        try:
            response = await openai.Image.acreate(prompt=prompt, n=n, size=size, response_format=response_format)

            if response_format == "url":
                return [d.url for d in response.data]

            return [d.b64_json for d in response.data]
        except Exception as e:
            raise APIError(f"Failed to generate image: {str(e)}") from e

    async def audio_transcription(
        self, audio_file: Union[str, Path], model: Optional[str] = None, language: Optional[str] = None
    ) -> str:
        """Transcribe audio.

        Args:
            audio_file: Path to audio file
            model: Transcription model
            language: Language code

        Returns:
            Transcribed text

        Raises:
            APIError: If request fails
        """
        try:
            with open(audio_file, "rb") as f:
                response = await openai.Audio.atranscribe(file=f, model=model or "whisper-1", language=language)
            return response.text
        except Exception as e:
            raise APIError(f"Failed to transcribe audio: {str(e)}") from e


def get_ai_processor(
    api_key: Optional[str] = None,
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: int = 2000,
    logger: Optional[logging.Logger] = None,
) -> AIProcessor:
    """Get an AI processor instance.

    Args:
        api_key: OpenAI API key
        model: Model name
        temperature: Temperature setting
        max_tokens: Maximum tokens
        logger: Logger instance

    Returns:
        AIProcessor instance
    """
    return AIProcessor(api_key=api_key, model=model, temperature=temperature, max_tokens=max_tokens, logger=logger)
