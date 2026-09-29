"""Application configuration module for RAGLift.

Centralized source of truth for environment variables loaded via Pydantic Settings.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """RAGLift Settings model validating environment variables."""

    # Embedding Provider Settings
    EMBEDDING_PROVIDER: str = "gemini"
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # Storage Paths
    CHROMA_PATH: str = "./data/chroma"
    BM25_INDEX_PATH: str = "./data/bm25_index.pkl"
    INGESTION_LOG_PATH: str = "./data/ingestion_log.jsonl"

    # Retrieval & Reranking Settings
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    TOP_K_RETRIEVE: int = 50
    TOP_K_RERANK: int = 5

    # Chunking Parameters
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    # System Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
