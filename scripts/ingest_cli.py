"""CLI script for ingesting document files directly into RAGLift without HTTP API calls.

Usage:
    python scripts/ingest_cli.py --path /path/to/docs/
"""

import argparse
import glob
import os
import sys

# Ensure root workspace directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas.ingest import DocumentInput
from app.services.ingestion_service import IngestionService


def main() -> None:
    parser = argparse.ArgumentParser(description="RAGLift CLI Document Ingestion Tool")
    parser.add_argument(
        "--path",
        required=True,
        help="Path to file or directory containing markdown/text documents to ingest",
    )
    args = parser.parse_args()

    target_path = os.path.abspath(args.path)
    if not os.path.exists(target_path):
        print(f"Error: Target path '{target_path}' does not exist.")
        sys.exit(1)

    files_to_read = []
    if os.path.isfile(target_path):
        files_to_read.append(target_path)
    else:
        for ext in ("*.md", "*.txt", "*.json"):
            files_to_read.extend(glob.glob(os.path.join(target_path, "**", ext), recursive=True))

    if not files_to_read:
        print(f"No text/markdown files found at '{target_path}'.")
        sys.exit(0)

    print(f"Found {len(files_to_read)} file(s) to ingest...")
    documents = []
    for filepath in files_to_read:
        doc_id = os.path.splitext(os.path.basename(filepath))[0]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                documents.append(
                    DocumentInput(
                        doc_id=doc_id,
                        text=content,
                        metadata={"source_path": filepath},
                    )
                )
        except Exception as e:
            print(f"Warning: Failed to read {filepath}: {e}")

    if not documents:
        print("No readable non-empty documents found.")
        sys.exit(0)

    service = IngestionService()
    response = service.ingest_documents(documents)
    print("Ingestion Complete!")
    print(f"  Processed Documents: {response.documents_processed}")
    print(f"  Total Chunks:        {response.total_chunks}")
    print(f"  Ingested At:         {response.ingested_at}")


if __name__ == "__main__":
    main()
