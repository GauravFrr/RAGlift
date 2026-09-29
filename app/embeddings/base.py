"""Abstract base class interface for embedding providers in RAGLift."""

from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """Abstract interface for text embedding providers.

    All embedding providers (Gemini, OpenAI, Local, Mock) must implement
    this interface to ensure provider swappability across RAGLift.
    """

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of document chunks.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of floating point embedding vectors.
        """
        pass

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Generate a vector embedding for a single search query.

        Args:
            text: Query string to embed.

        Returns:
            Single floating point embedding vector.
        """
        pass
