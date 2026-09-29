.PHONY: up down test eval lint ingest reset help

help:
	@echo "RAGLift Commands:"
	@echo "  make up       - Build and start Docker services"
	@echo "  make down     - Stop Docker services"
	@echo "  make test     - Run pytest test suite"
	@echo "  make eval     - Run standalone evaluation benchmark"
	@echo "  make lint     - Run code linting check"
	@echo "  make ingest   - Ingest default demo corpus via CLI"
	@echo "  make reset    - Reset ChromaDB and BM25 index"

up:
	docker-compose up --build

down:
	docker-compose down

test:
	pytest -v tests/

eval:
	python eval/run_eval.py

lint:
	python -m ruff check app/ scripts/ tests/ || ruff check app/ scripts/ tests/

ingest:
	python scripts/ingest_cli.py --path eval/sample_corpus/

reset:
	python scripts/reset_index.py
