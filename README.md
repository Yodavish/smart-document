# Smart Document

A Python document-processing and retrieval-augmented generation (RAG) project for extracting, indexing, searching, and querying PDF documents with a locally hosted LLM.

The current implementation processes a PDF, extracts text with PyMuPDF and Tesseract OCR, splits the text into chunks, generates local vector embeddings, stores them in ChromaDB, retrieves relevant passages using semantic similarity, and sends the retrieved context to GPT-OSS 20B through Ollama.

## Current Pipeline

```text
PDF
 ↓
PyMuPDF text extraction
 ↓
Tesseract OCR fallback
 ↓
LangChain text chunking
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

* Opens PDF documents using PyMuPDF
* Extracts existing text directly from PDF pages
* Detects pages without a usable text layer
* Converts scanned PDF pages into images
* Uses Tesseract OCR for scanned pages
* Supports multi-page PDF documents
* Splits extracted text using LangChain's `RecursiveCharacterTextSplitter`
* Uses overlapping text chunks to preserve context between chunks
* Preserves PDF page numbers as chunk metadata
* Generates local 384-dimensional embeddings using `all-MiniLM-L6-v2`
* Stores document chunks, embeddings, and metadata in persistent ChromaDB
* Performs semantic similarity searches against document content
* Uses Ollama to run GPT-OSS 20B locally
* Generates answers using retrieved document context
* Supports an interactive question-and-answer loop
* Runs the RAG pipeline locally without requiring a cloud LLM API

Ollama provides a local API that applications can use to interact with locally running models. The Python client is used by this project to send retrieved document context to GPT-OSS 20B.

## Example

The application can answer questions about the contents of the processed document:

```text
How may I help you? Who wrote Questioned Documents?

--- Answer ---
Albert S. Osborn.
```

It can also answer questions requiring information from specific portions of the document, such as:

```text
How may I help you? What happened in Oles v. Wilson?

--- Answer ---
In Oles v. Wilson, Judge Strong of the Colorado district court
decided the case in December 1916 and declined to open the
civil proceeding...
```

## Current Limitations

The current version is a baseline RAG system.

* OCR image preprocessing has not yet been implemented
* OCR text cleanup has not yet been implemented
* Retrieval currently relies on semantic similarity
* Page-specific queries are not yet handled using metadata filtering
* The application currently processes the document again when the program starts
* Chroma document IDs are currently generated from chunk indexes
* The application currently processes one configured PDF
* Retrieved sources are not yet displayed with the final answer
* There is no web interface yet
* There is no document upload interface yet

These limitations maybe will be addressed in later iterations.

## Technology

### Python

* Python 3.14+
* PyMuPDF
* Pillow
* pytesseract
* LangChain Text Splitters
* Sentence Transformers
* ChromaDB
* Ollama Python client

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

* Python 3.14+
* Tesseract OCR
* Ollama
* NVIDIA GPU recommended for local LLM inference

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

```bash
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
Pages: 584
Chunks: 1205
Embeddings: 1205
Vector dimensions: 384

How may I help you? Who wrote Questioned Documents?

--- Answer ---
Albert S. Osborn.
```

## Project Status

This project is mainly for study and currently has a working end-to-end local RAG pipeline:

**PDF → OCR → chunking → embeddings → ChromaDB → retrieval → Ollama → LLM response**
