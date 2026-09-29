"""Unit tests for Cross-Encoder reranker."""

from unittest.mock import MagicMock, patch

from app.retrieval.reranker import Reranker


@patch("app.retrieval.reranker.CrossEncoder")
def test_reranker_reorders_candidates(mock_cross_encoder):
    """Verify that Reranker reorders candidates based on mock cross-encoder predictions."""
    mock_instance = MagicMock()
    # Return higher score for candidate 2 than candidate 1
    mock_instance.predict.return_value = [0.1, 0.9]
    mock_cross_encoder.return_value = mock_instance

    reranker = Reranker(model_name="dummy-model")

    candidates = [
        ("chunk_1", 0.03, "Python coding tutorial", {"doc_id": "doc1"}),
        ("chunk_2", 0.02, "FastAPI authentication guide", {"doc_id": "doc2"}),
    ]

    reranked = reranker.rerank(
        query="How to authenticate in FastAPI", candidates=candidates, top_k=2
    )

    assert len(reranked) == 2
    assert reranked[0][0] == "chunk_2"  # Predict score 0.9
    assert reranked[1][0] == "chunk_1"  # Predict score 0.1
