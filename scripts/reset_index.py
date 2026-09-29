"""CLI script to reset/wipe RAGLift vector storage, BM25 index, and ingestion logs.

Usage:
    python scripts/reset_index.py
"""

import os
import shutil
import sys

# Ensure root workspace directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.retrieval.bm25 import BM25Index
from app.retrieval.dense import DenseRetriever


def reset_all() -> None:
    """Clear BM25 index, ChromaDB persistent store, and ingestion logs."""
    print("Resetting RAGLift indexes...")

    # Clear BM25 index
    bm25 = BM25Index()
    bm25.clear()
    print("  [x] BM25 Index cleared.")

    # Clear ChromaDB
    dense = DenseRetriever()
    dense.clear()
    print("  [x] ChromaDB Vector Store cleared.")

    # Remove ChromaDB persistence directory if exists
    if os.path.exists(settings.CHROMA_PATH):
        try:
            shutil.rmtree(settings.CHROMA_PATH)
            print(f"  [x] Removed Chroma directory: {settings.CHROMA_PATH}")
        except Exception as e:
            print(f"  [!] Warning removing Chroma directory: {e}")

    # Remove ingestion log if exists
    if os.path.exists(settings.INGESTION_LOG_PATH):
        try:
            os.remove(settings.INGESTION_LOG_PATH)
            print(f"  [x] Removed Ingestion Log: {settings.INGESTION_LOG_PATH}")
        except Exception as e:
            print(f"  [!] Warning removing Ingestion Log: {e}")

    print("Reset completed successfully!")


if __name__ == "__main__":
    reset_all()
