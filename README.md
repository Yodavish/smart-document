# Smart Document

A Python study project built to understand the core components of a local retrieval-augmented generation (RAG) pipeline.

The application processes PDF documents, extracts text using PyMuPDF and Tesseract OCR, splits the text into chunks, generates local vector embeddings, stores them in ChromaDB, retrieves relevant passages using semantic similarity, and sends the retrieved context to a locally hosted GPT-OSS 20B model through Ollama.

## Current Pipeline

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
ChromaDB vector storage
 ↓
Semantic similarity retrieval
 ↓
Retrieved context
 ↓
Ollama / GPT-OSS 20B
 ↓
Generated answer
```

## Current Features

- Opens PDF documents using PyMuPDF
- Extracts existing text directly from PDF pages
- Detects pages without a usable text layer
- Converts scanned PDF pages into images
- Uses Tesseract OCR for scanned pages
- Supports multi-page PDF documents
- Splits extracted text using LangChain's `RecursiveCharacterTextSplitter`
- Uses overlapping text chunks to preserve context between chunks
- Preserves PDF page numbers as chunk metadata
- Generates local 384-dimensional embeddings using `all-MiniLM-L6-v2`
- Stores document chunks, embeddings, and metadata in persistent ChromaDB
- Performs semantic similarity searches against document content
- Uses Ollama to run GPT-OSS 20B locally
- Generates answers using retrieved document context
- Supports an interactive question-and-answer loop
- Runs the RAG pipeline locally without requiring a cloud LLM API

Ollama provides a local API that applications can use to interact with locally running models. The Python client is used by this project to send retrieved document context to GPT-OSS 20B.

## Example

The application can answer questions about the contents of the processed document:

```text
How may I help you? Who wrote Questioned Documents?

--- Answer ---

Albert S. Osborn.
```

It can also retrieve information from specific portions of the document:

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

## Retrieval

The project uses semantic similarity retrieval rather than traditional keyword search.

Each document chunk is converted into a 384-dimensional vector using `all-MiniLM-L6-v2` and stored in ChromaDB.

When a user submits a question, the question is converted into a vector using the same embedding model. ChromaDB then performs nearest-neighbor retrieval to find the most semantically similar document chunks.

```text
Document Chunk
     ↓
Embedding Model
     ↓
384-dimensional vector
     ↓
ChromaDB


User Question
     ↓
Embedding Model
     ↓
384-dimensional query vector
     ↓
Semantic similarity search
     ↓
Top matching chunks
     ↓
Ollama
```

The current implementation retrieves the five most relevant chunks for each question.

## What I Learned

This project was built as a study project to understand the underlying components of RAG rather than relying on a high-level RAG framework to abstract away the retrieval process.

Key concepts explored:

- PDF text extraction and OCR fallback
- Processing scanned PDF documents
- Text chunking and chunk overlap
- Recursive character-based text splitting
- Text embeddings and vector representations
- 384-dimensional embeddings using `all-MiniLM-L6-v2`
- Persistent vector storage using ChromaDB
- KNN-based semantic similarity retrieval
- Query embeddings
- Retrieving relevant document context
- Passing retrieved context to an LLM
- Running an LLM locally using Ollama
- Building an end-to-end local RAG pipeline

## Current Limitations

The current version is a baseline RAG system intentionally kept simple for learning purposes.

- OCR image preprocessing is outside the current scope
- OCR text cleanup is outside the current scope
- Retrieval currently relies on semantic similarity
- Page-specific queries are not yet handled using metadata filtering
- The document is reprocessed when the application starts
- ChromaDB document IDs are currently generated from chunk indexes
- The application currently processes one configured PDF
- Retrieved sources are not displayed with the final answer
- There is no web interface
- There is no document upload interface

These features are outside the current scope of this study project.

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

### Local AI

**Embedding model**

```text
sentence-transformers/all-MiniLM-L6-v2
```

Produces 384-dimensional document embeddings.

**LLM**

```text
gpt-oss:20b
```

Runs locally through Ollama.

## Requirements

- Python 3.14+
- Tesseract OCR
- Ollama
- NVIDIA GPU recommended for local LLM inference

## Installation

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```powershell
.venv\Scripts\activate
```

Install the Python dependencies:

```powershell
pip install pymupdf pillow pytesseract langchain-text-splitters sentence-transformers chromadb ollama
```

Install Tesseract OCR separately and configure the executable path in the project.

Install Ollama and download the model:

```powershell
ollama run gpt-oss:20b
```

Ollama must be installed and running locally for the LLM portion of the application.

## Usage

Run the application:

```powershell
python smart_doc.py
```

The application will:

1. Open the configured PDF.
2. Extract native PDF text.
3. Use Tesseract when a page has no usable text layer.
4. Split the extracted text into chunks.
5. Generate vector embeddings.
6. Store the chunks and embeddings in ChromaDB.
7. Accept questions through the interactive prompt.
8. Retrieve the most relevant document chunks.
9. Send the retrieved context to GPT-OSS 20B.
10. Return the generated answer.

Example:

```text
How may I help you? Who wrote Questioned Documents?

--- Answer ---

Albert S. Osborn.
```

## Project Status

Complete study project demonstrating a working end-to-end local RAG pipeline.

**PDF → OCR → Chunking → Embeddings → ChromaDB → Semantic Retrieval → Ollama → LLM Response**

The project is intentionally kept simple to demonstrate the underlying RAG components rather than production features.