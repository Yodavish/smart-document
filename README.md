# Smart Document

A Python document-processing project for extracting, processing, and eventually searching text from PDF documents. The project currently supports standard PDF text extraction with Tesseract OCR as a fallback for scanned pages.

## Current Features

* Opens PDF documents using PyMuPDF
* Extracts existing text directly from PDF pages
* Detects pages without a usable text layer
* Converts scanned PDF pages into images
* Uses Tesseract OCR to extract text from scanned pages
* Saves extracted document text to a text file
* Supports multi-page PDF documents

## Planned Features

* Process multiple PDF documents
* Split extracted text into chunks
* Generate vector embeddings
* Store embeddings in a vector database
* Search documents using semantic similarity
* Integrate Ollama for local LLM-based question answering
* Return answers based on relevant document content

## Requirements

* Python 3.14+
* Tesseract OCR

### Python Packages

* PyMuPDF
* Pillow
* pytesseract

## Installation

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```powershell
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install pymupdf pillow pytesseract
```

Install Tesseract OCR separately and make sure the executable path is configured in the project.

## Usage

Run the application with a PDF document:

```bash
python smart_doc.py
```

The application extracts text from the PDF. Pages with an existing text layer use PyMuPDF text extraction. Scanned pages fall back to Tesseract OCR.

Extracted text is saved to:

```text
output/result.txt
```

## Project Status

The current implementation focuses on PDF text extraction and OCR. The next stage will focus on document chunking and vector embeddings before adding semantic search and Ollama-based question answering.
