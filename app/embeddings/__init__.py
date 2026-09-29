"""Embedding module initialization and factory function."""

from app.core.config import settings
from app.core.logging import logger
from app.embeddings.base import EmbeddingProvider
from app.embeddings.gemini_provider import GeminiEmbeddingProvider
from app.embeddings.local_provider import LocalEmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    """Deterministic mock embedding provider for quick offline testing."""

    def __init__(self, dimension: int = 768):
        self.dimension = dimension

    def _hash_text(self, text: str) -> list[float]:
        import hashlib

        h = hashlib.sha256(text.encode("utf-8")).digest()
        vec = [(float(b) / 255.0) - 0.5 for b in h]
        while len(vec) < self.dimension:
            vec.extend(vec)
        return vec[: self.dimension]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._hash_text(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._hash_text(text)


def get_embedding_provider() -> EmbeddingProvider:
    """Factory function returning the configured EmbeddingProvider instance."""
    provider_name = settings.EMBEDDING_PROVIDER.lower()

    if provider_name == "gemini":
        if not settings.GEMINI_API_KEY:
            logger.info(
                "GEMINI_API_KEY not set. Defaulting to local SentenceTransformer embeddings."
            )
            return LocalEmbeddingProvider()
        return GeminiEmbeddingProvider()
    elif provider_name in ("local", "sentence-transformers"):
        return LocalEmbeddingProvider()
    elif provider_name in ("mock", "test"):
        return MockEmbeddingProvider()
    else:
        raise ValueError(
            f"Unsupported EMBEDDING_PROVIDER '{provider_name}'. "
            "Supported values are 'gemini', 'local', 'mock'."
        )


__all__ = [
    "EmbeddingProvider",
    "GeminiEmbeddingProvider",
    "LocalEmbeddingProvider",
    "MockEmbeddingProvider",
    "get_embedding_provider",
]
