from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
# helps define expected request structure
from pydantic import BaseModel
from smart_doc import DocumentProcessor
import os
import shutil

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = "uploads"
CHROMA_DIRECTORY = "chroma_db"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

class QueryRequest(BaseModel):
    question: str

doc = None

@app.post("/api/upload")
def upload_document(file: UploadFile = File(...)):

    global doc
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create processor for uploaded document
    doc = DocumentProcessor(file_path)
    doc.reset_collection()
    doc.open_documents()
    doc.extract_pages()
    doc.chunk_text()
    embeddings = doc.embed_chunks()
    doc.store_embeddings(embeddings)

    return {
        "filename": file.filename,
        "pages": len(doc.page_text),
        "chunks": len(doc.chunks),
        "message": "Document processed successfully"
    }



@app.post("/api/query")
def query_document(request: QueryRequest):
    if doc is None:
        return {"error": "No document has been imported."}
    results = doc.retrieve(request.question)
    context = "\n\n".join(results["documents"][0])
    answer = doc.generate_answer(
        request.question,
        context
    )

    return {
        "answer": answer,
        "chunks": results["documents"][0],
        "distances": results["distances"][0],
    }