# Smart Document

A Python study project built to understand the core components of a local retrieval-augmented generation (RAG) pipeline.

The application processes PDF documents, extracts text using PyMuPDF and Tesseract OCR, splits the text into chunks, generates local vector embeddings, stores them in ChromaDB, retrieves relevant passages using semantic similarity, and sends the retrieved context to a locally hosted GPT-OSS 20B model through Ollama.

The project also includes a Docker containerization setup to learn how to package and run the application in an isolated Linux environment while connecting to Ollama running on the host machine.

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
* Runs the application inside a Docker container
* Installs Tesseract inside the Docker image
* Uses a Docker bind mount for PDF documents
* Uses a persistent Docker volume for ChromaDB
* Connects from the Docker container to Ollama running on the host machine

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

* PDF text extraction and OCR fallback
* Processing scanned PDF documents
* Text chunking and chunk overlap
* Recursive character-based text splitting
* Text embeddings and vector representations
* 384-dimensional embeddings using `all-MiniLM-L6-v2`
* Persistent vector storage using ChromaDB
* KNN-based semantic similarity retrieval
* Query embeddings
* Retrieving relevant document context
* Passing retrieved context to an LLM
* Running an LLM locally using Ollama
* Building an end-to-end local RAG pipeline
* Building a Docker image
* Running a Python application inside a Docker container
* Installing system dependencies such as Tesseract inside a Docker image
* Using Docker bind mounts for application data
* Using Docker named volumes for persistent data
* Connecting a container to a service running on the host machine

## Docker Architecture

The application uses Docker to run the Python application and its dependencies inside a Linux container.

Ollama remains installed on the Windows host because it handles the local GPT-OSS 20B inference.

```text
Windows Host
│
├── Docker Desktop
│   │
│   └── Smart Document Container
│       ├── Python
│       ├── Tesseract
│       ├── Python dependencies
│       └── smart_doc.py
│
├── test_data/
│   └── Questioned_documents.pdf
│       │
│       └── Bind mount → /app/test_data
│
├── Docker Volume
│   └── smart-document-chroma
│       │
│       └── Mount → /app/chroma_db
│
└── Ollama
    └── GPT-OSS 20B
        ↑
        │
        └── host.docker.internal:11434
```

The PDF is provided to the container using a bind mount rather than being included in the Docker image.

ChromaDB uses a Docker named volume so vector data persists after the application container is removed.

The container connects to Ollama using Docker Desktop's `host.docker.internal` hostname, which resolves to the host machine from inside the container.

## Current Limitations

The current version is a baseline RAG system intentionally kept simple for learning purposes.

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

### Containerization

* Docker Desktop
* Python 3.14 Linux container
* Tesseract OCR installed through the Linux package manager
* Docker bind mounts
* Docker named volumes
* Docker-to-host networking

## Requirements

### Running Without Docker

* Python 3.14+
* Tesseract OCR
* Ollama
* NVIDIA GPU recommended for local LLM inference

### Running With Docker

* Docker Desktop
* Ollama installed on the host machine
* GPT-OSS 20B downloaded through Ollama
* NVIDIA GPU recommended for local LLM inference

Docker Desktop for Windows provides the Docker Engine and Linux container environment used by this project.

## Installation

### Option 1: Run Directly with Python

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

#### Windows

```powershell
.venv\Scripts\activate
```

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

Install Tesseract OCR separately.

Install Ollama and download the model:

```powershell
ollama run gpt-oss:20b
```

Ollama must be installed and running locally for the LLM portion of the application.

Run the application:

```powershell
python smart_doc.py
```

### Option 2: Run with Docker

Build the Docker image from the project directory:

```powershell
docker build -t smart-document .
```

Create a persistent Docker volume for ChromaDB:

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

The first mount provides the PDF from the Windows host:

```text
Windows
C:\GitHubProjects\smart-document\test_data
        ↓
Container
/app/test_data
```

The second mount provides persistent storage for ChromaDB:

```text
Docker volume
smart-document-chroma
        ↓
Container
/app/chroma_db
```

The application connects to Ollama on the Windows host through:

```text
http://host.docker.internal:11434
```

Docker Desktop provides `host.docker.internal` for containers that need to connect to services running on the host.

## Usage

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

## Project Files

```text
smart-document/
├── test_data/
│   └── Questioned_documents.pdf
├── smart_doc.py
├── requirements.txt
├── README.md
├── Dockerfile
└── .dockerignore
```

The local `.venv/` and `chroma_db/` directories are excluded from the Docker build context.

PDF files are also excluded from the Docker image and supplied through a bind mount when running the container.

## Project Status

Complete study project demonstrating a working end-to-end local RAG pipeline and Docker containerization.

**PDF → OCR → Chunking → Embeddings → ChromaDB → Semantic Retrieval → Ollama → LLM Response**

The project is intentionally kept simple to demonstrate the underlying RAG and containerization concepts rather than production features.
