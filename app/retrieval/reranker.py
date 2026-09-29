"""Cross-encoder reranking module for RAGLift.

Re-scores top candidate chunks from RRF fusion using a transformer Cross-Encoder model.
"""

from typing import Any, Dict, List, Tuple

from sentence_transformers import CrossEncoder

from app.core.config import settings
from app.core.logging import logger


class Reranker:
    """Transformer Cross-Encoder reranker."""

    def __init__(self, model_name: str = None):
        """Initialize Cross-Encoder model instance.

        Args:
            model_name: HuggingFace cross-encoder model name. Defaults to settings.RERANKER_MODEL.
        """
        self.model_name = model_name or settings.RERANKER_MODEL
        self._model: CrossEncoder = None

    def _get_model(self) -> CrossEncoder:
        """Lazy load CrossEncoder model on first call to save memory during startup."""
        if self._model is None:
            logger.info("Loading CrossEncoder model '%s'...", self.model_name)
            self._model = CrossEncoder(self.model_name)
        return self._model

    def rerank(
        self,
        query: str,
        candidates: List[Tuple[str, float, str, Dict[str, Any]]],
        top_k: int = 5,
    ) -> List[Tuple[str, float, str, Dict[str, Any]]]:
        """Rerank candidate chunks using Cross-Encoder self-attention over (query, document) pairs.

        Why Cross-Encoder Reranking is the final secret sauce:
        1. Bi-encoders (dense vector search) compress query and document into separate
           vector points, sacrificing fine-grained cross-token attention interactions.
        2. Cross-encoders feed query + text into transformer self-attention layers together,
           evaluating exact semantic alignment, negation, conditionality, and context.
        3. Running cross-encoding only on top-50 fused candidates provides maximum recall
           boost without latency penalties of scanning the full collection.

        Args:
            query: Search query text.
            candidates: Fused candidate list of (chunk_id, rrf_score, text, metadata).
            top_k: Number of final top reranked chunks to return.

        Returns:
            Reranked list of tuples: (chunk_id, score, text, metadata) sorted descending.
        """
        if not candidates:
            return []

        model = self._get_model()

        # Construct (query, text) sentence pairs for cross-encoder inference
        pairs = [(query, text) for _, _, text, _ in candidates]
        scores = model.predict(pairs)

        # Pair candidates with new cross-encoder scores
        scored_candidates = []
        for (chunk_id, _, text, metadata), score in zip(candidates, scores):
            scored_candidates.append((chunk_id, float(score), text, metadata))

        # Sort descending by cross-encoder score
        reranked = sorted(scored_candidates, key=lambda x: x[1], reverse=True)

        return reranked[:top_k]
