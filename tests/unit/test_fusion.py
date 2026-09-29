"""Unit tests for Reciprocal Rank Fusion (RRF) logic."""

from app.retrieval.fusion import rrf_fuse


def test_rrf_fuse_combines_and_ranks_candidates():
    """Verify that RRF fusion correctly computes reciprocal rank scores."""
    bm25_results = [
        ("doc_1", 10.5, "Text 1", {"source": "bm25"}),
        ("doc_2", 8.2, "Text 2", {"source": "bm25"}),
    ]

    dense_results = [
        ("doc_2", 0.95, "Text 2", {"source": "dense"}),
        ("doc_3", 0.88, "Text 3", {"source": "dense"}),
    ]

    # Run RRF fusion with k=60
    fused = rrf_fuse(bm25_results=bm25_results, dense_results=dense_results, k=60, top_k=5)

    # doc_2 is rank 2 in BM25 (1/(60+2) = 1/62) and rank 1 in Dense (1/(60+1) = 1/61)
    # doc_1 is rank 1 in BM25 only (1/61)
    # doc_3 is rank 2 in Dense only (1/62)
    # doc_2 should have highest fused score and be at rank 1

    assert len(fused) == 3
    top_chunk_id, top_score, top_text, _ = fused[0]
    assert top_chunk_id == "doc_2"
    assert top_score > (1.0 / 61.0)


def test_rrf_fuse_handles_empty_inputs():
    """Verify RRF fusion when one or both result lists are empty."""
    bm25_results = [("doc_1", 5.0, "Text 1", {})]
    dense_results = []

    fused = rrf_fuse(bm25_results, dense_results)
    assert len(fused) == 1
    assert fused[0][0] == "doc_1"

    empty_fused = rrf_fuse([], [])
    assert empty_fused == []
