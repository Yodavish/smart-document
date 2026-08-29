# Smart Document

A Python study project built to understand the core components of a local retrieval-augmented generation (RAG) pipeline.

The application processes PDF documents, extracts text using PyMuPDF and Tesseract OCR, splits the text into chunks, generates vector embeddings, stores them in ChromaDB, retrieves relevant passages using semantic similarity, and sends the retrieved context to a locally hosted GPT-OSS 20B model through Ollama.

The project also includes Docker containerization to run the application in an isolated Linux environment while connecting to Ollama running on the host machine.

## Pipeline

```text
PDF
 ↓
PyMuPDF text extraction
 ↓
Tesseract OCR fallback
 ↓
Recursive character chunking
 ↓
Sentence Transformers embeddings
 ↓
ChromaDB
 ↓
Semantic similarity retrieval
 ↓
Retrieved context
 ↓
Ollama / GPT-OSS 20B
 ↓
Generated answer
```

## Features

- PDF text extraction with PyMuPDF
- Tesseract OCR fallback for scanned pages
- Recursive character text splitting with chunk overlap
- PDF page metadata preserved with chunks
- 384-dimensional embeddings using `all-MiniLM-L6-v2`
- Persistent ChromaDB vector storage
- Semantic similarity retrieval using nearest-neighbor search
- Local GPT-OSS 20B inference through Ollama
- Interactive question-and-answer interface
- Dockerized application environment
- Docker bind mount for document data
- Docker volume for persistent ChromaDB data

## Example

```text
How may I help you? Who wrote Questioned Documents?

--- Answer ---

Albert S. Osborn.
```

The system can also retrieve information from specific sections of the document:

```text
How may I help you? What are the different classes of questioned documents?

--- Answer ---

The different classes of questioned documents are:

1. Documents with questioned signatures
2. Documents containing alleged fraudulent alterations
3. Holograph documents questioned or disputed
4. Documents attacked on the question of their age or date
5. Documents attacked on the question of materials used in their production
6. Documents investigated on the question of typewriting
7. Documents or writings investigated because they identify some person through handwriting
```

## What I Learned

This project was built to understand the underlying components of RAG rather than relying on a high-level framework to abstract away the retrieval process.

- OCR and PDF text extraction
- Text chunking and overlap
- Vector embeddings
- 384-dimensional vector representations
- Semantic similarity retrieval
- KNN / nearest-neighbor search
- Query embeddings
- Vector databases
- Retrieval-augmented generation
- Local LLM inference
- Docker containerization
- Docker bind mounts and named volumes
- Container-to-host networking

## Technology

### Python

- Python 3.14+
- PyMuPDF
- Pillow
- pytesseract
- LangChain Text Splitters
- Sentence Transformers
- ChromaDB
- Ollama Python client

### Models

**Embedding**

```text
sentence-transformers/all-MiniLM-L6-v2
```

**LLM**

```text
gpt-oss:20b
```

### Containerization

- Docker Desktop
- Python 3.14 Linux container
- Tesseract OCR
- Docker bind mounts
- Docker named volumes

## Running Locally

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Install Tesseract OCR and Ollama separately.

Download the model:

```powershell
ollama run gpt-oss:20b
```

Run the application:

```powershell
python smart_doc.py
```

## Running with Docker

Build the image:

```powershell
docker build -t smart-document .
```

Create the ChromaDB volume:

```powershell
docker volume create smart-document-chroma
```

Run the container:

```powershell
docker run -it --rm `
  -v "${PWD}\test_data:/app/test_data" `
  -v "smart-document-chroma:/app/chroma_db" `
  smart-document
```

The PDF is provided through a Docker bind mount and ChromaDB uses a persistent Docker volume.

Ollama remains on the Windows host and the container connects to it through:

```text
http://host.docker.internal:11434
```

## Current Limitations

This is intentionally a small study project rather than a production RAG application.

- No OCR preprocessing or cleanup
- Semantic retrieval only
- No metadata filtering
- One configured PDF
- Document is reprocessed when the application starts
- Retrieved sources are not displayed with the answer
- No web interface or document upload system

## Project Status

Complete study project demonstrating an end-to-end local RAG pipeline and Docker containerization.

**PDF → OCR → Chunking → Embeddings → ChromaDB → Semantic Retrieval → Ollama → LLM Response**
