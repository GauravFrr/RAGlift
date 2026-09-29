"""Reciprocal Rank Fusion (RRF) module for hybrid retrieval.

Combines separate candidate result lists from keyword search (BM25) and dense vector
search (ChromaDB) into a single unified rank list.
"""

from typing import Any, Dict, List, Tuple


def rrf_fuse(
    bm25_results: List[Tuple[str, float, str, Dict[str, Any]]],
    dense_results: List[Tuple[str, float, str, Dict[str, Any]]],
    k: int = 60,
    top_k: int = 50,
) -> List[Tuple[str, float, str, Dict[str, Any]]]:
    """Combine BM25 and Dense search candidate lists using Reciprocal Rank Fusion.

    Why RRF over Simple Score Averaging:
    1. Score Scale Incompatibility: BM25 scores (unbounded) and vector cosine similarity
       ([0, 1]) exist on entirely different mathematical scales. Normalizing raw scores is
       fragile and sensitive to outlier query scores.
    2. Rank-Based Neutrality: RRF operates exclusively on relative positions (ranks),
       eliminating score calibration issues.
    3. Formula: RRF_score(doc) = sum(1 / (k + rank(doc))), where k=60 is the standard
       smoothing constant proved by Cormack et al. to balance top ranks gracefully.

    Args:
        bm25_results: Ranked list of (chunk_id, score, text, metadata) from BM25.
        dense_results: Ranked list of (chunk_id, score, text, metadata) from Dense vector search.
        k: Smoothing constant in RRF formula (default 60).
        top_k: Number of fused candidates to return.

    Returns:
        Fused list of tuples: (chunk_id, rrf_score, text, metadata) sorted by rrf_score descending.
    """
    fused_scores: Dict[str, float] = {}
    doc_map: Dict[str, Tuple[str, Dict[str, Any]]] = {}

    # Accumulate RRF scores from BM25 ranks
    for rank, (chunk_id, _, text, metadata) in enumerate(bm25_results, start=1):
        rrf_contrib = 1.0 / (k + rank)
        fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + rrf_contrib
        if chunk_id not in doc_map:
            doc_map[chunk_id] = (text, metadata)

    # Accumulate RRF scores from Dense ranks
    for rank, (chunk_id, _, text, metadata) in enumerate(dense_results, start=1):
        rrf_contrib = 1.0 / (k + rank)
        fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + rrf_contrib
        if chunk_id not in doc_map:
            doc_map[chunk_id] = (text, metadata)

    # Sort candidates by combined RRF score descending
    sorted_chunk_ids = sorted(fused_scores.keys(), key=lambda cid: fused_scores[cid], reverse=True)

    fused_candidates = []
    for chunk_id in sorted_chunk_ids[:top_k]:
        text, metadata = doc_map[chunk_id]
        score = fused_scores[chunk_id]
        fused_candidates.append((chunk_id, score, text, metadata))

    return fused_candidates
