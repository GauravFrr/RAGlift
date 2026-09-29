"""Pydantic schemas for ingestion request and response models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentInput(BaseModel):
    """Input representation of a document to ingest."""

    doc_id: str = Field(..., description="Unique document identifier")
    text: str = Field(..., description="Full text content of the document")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Optional document metadata key-value pairs"
    )


class IngestRequest(BaseModel):
    """Request model for POST /ingest endpoint."""

    documents: List[DocumentInput] = Field(..., description="List of documents to chunk and index")
    chunk_size: Optional[int] = Field(
        None, description="Override default chunk size in tokens/words"
    )
    chunk_overlap: Optional[int] = Field(None, description="Override default chunk overlap")


class IngestResponse(BaseModel):
    """Response model for POST /ingest endpoint."""

    status: str = Field("success", description="Ingestion execution status")
    documents_processed: int = Field(..., description="Number of source documents processed")
    total_chunks: int = Field(..., description="Total number of chunks generated and indexed")
    ingested_at: str = Field(..., description="ISO 8601 timestamp of ingestion completion")
