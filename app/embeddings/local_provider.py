"""Local embedding provider implementation using SentenceTransformers."""

from typing import List

from sentence_transformers import SentenceTransformer

from app.core.logging import logger
from app.embeddings.base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):
    """Local embedding provider using SentenceTransformers all-MiniLM-L6-v2 model.

    Runs 100% locally without external API keys or network dependencies.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize SentenceTransformer model for local embedding generation."""
        self.model_name = model_name
        logger.info("Loading local embedding model '%s'...", self.model_name)
        self.model = SentenceTransformer(self.model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of document strings."""
        if not texts:
            return []
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Generate vector embedding for a single search query."""
        embedding = self.model.encode(text, show_progress_bar=False, convert_to_numpy=True)
        return embedding.tolist()
