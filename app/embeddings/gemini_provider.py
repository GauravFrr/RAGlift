"""Gemini embedding provider implementation for RAGLift."""

from typing import List

import google.generativeai as genai

from app.core.config import settings
from app.embeddings.base import EmbeddingProvider


class GeminiEmbeddingProvider(EmbeddingProvider):
    """Embedding provider implementation using Google Gemini text-embedding-004 model.

    Default embedding provider for RAGLift.
    """

    def __init__(self, api_key: str = None, model_name: str = "models/text-embedding-004"):
        """Initialize the Gemini embedding provider with API key and target model.

        Args:
            api_key: Gemini API key. Defaults to settings.GEMINI_API_KEY.
            model_name: Model identifier for embedding generation.
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured. Please set GEMINI_API_KEY in your .env file."
            )
        self.model_name = model_name
        genai.configure(api_key=self.api_key)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of document strings using Gemini.

        Args:
            texts: List of document chunk texts.

        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []

        # Use batch embedding call from google-generativeai
        result = genai.embed_content(
            model=self.model_name,
            content=texts,
            task_type="retrieval_document"
        )
        return result["embedding"]

    def embed_query(self, text: str) -> List[float]:
        """Generate vector embedding for a single search query using Gemini.

        Args:
            text: Search query string.

        Returns:
            Single vector embedding.
        """
        result = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_query"
        )
        return result["embedding"]
