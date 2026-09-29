"""Integration smoke test for RAGLift.

Tests document ingestion and query retrieval end-to-end.
"""

import pytest
from fastapi.testclient import TestClient

from app.embeddings import MockEmbeddingProvider
from app.main import app
from app.schemas.ingest import DocumentInput
from app.services.ingestion_service import IngestionService
from app.services.retrieval_service import RetrievalService


def create_test_services(tmp_path):
    """Helper function creating isolated services backed by temporary disk storage."""
    chroma_dir = str(tmp_path / "chroma")
    bm25_file = str(tmp_path / "bm25.pkl")

    from app.retrieval.bm25 import BM25Index
    from app.retrieval.dense import DenseRetriever

    provider = MockEmbeddingProvider()
    bm25 = BM25Index(index_path=bm25_file)
    dense = DenseRetriever(chroma_path=chroma_dir, provider=provider)

    ingest_svc = IngestionService(provider=provider, bm25_index=bm25, dense_retriever=dense)
    retrieval_svc = RetrievalService(provider=provider, bm25_index=bm25, dense_retriever=dense)

    return ingest_svc, retrieval_svc


@pytest.fixture
def mock_services(tmp_path):
    """Fixture providing isolated services backed by temporary disk storage."""
    return create_test_services(tmp_path)


def test_health_endpoint():
    """Verify /health endpoint returns HTTP 200 ok."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ingestion_and_query_smoke(mock_services):
    """End-to-end smoke test: Ingest documents -> Query retrieval -> Validate result."""
    ingest_svc, retrieval_svc = mock_services

    docs = [
        DocumentInput(
            doc_id="doc_auth",
            text="API authentication requires a Bearer token in the Authorization header.",
            metadata={"category": "security"},
        ),
        DocumentInput(
            doc_id="doc_billing",
            text="Subscriptions can be upgraded or canceled from the billing settings tab.",
            metadata={"category": "billing"},
        ),
    ]

    # Run Ingestion
    ingest_res = ingest_svc.ingest_documents(docs, chunk_size=50, chunk_overlap=5)
    assert ingest_res.status == "success"
    assert ingest_res.documents_processed == 2
    assert ingest_res.total_chunks == 2

    # Run Query
    from app.schemas.query import QueryRequest

    query_req = QueryRequest(query="How do I handle API authentication?", use_reranker=False)
    query_res = retrieval_svc.query(query_req)

    assert query_res.query == "How do I handle API authentication?"
    assert query_res.total_results > 0
    # Top chunk should belong to auth doc
    assert query_res.results[0].doc_id == "doc_auth"
