# Multimodal RAG & Visual Document Intelligence

A local PDF ingestion and page-retrieval baseline. It renders each PDF page to an image, extracts page text, indexes text for transparent retrieval, and returns page image paths as visual evidence. This starter is useful without paid model APIs. It is **not yet ColPali or vision-embedding retrieval**; the retriever interface is the extension point for those models.

## Run
```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```
Upload a PDF to POST /ingest, then query POST /query. Files are stored under `data/`; keep this API private when processing sensitive documents.
