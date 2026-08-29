import pymupdf
import pytesseract

from io import BytesIO
from PIL import Image

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

import chromadb
import ollama

ollama_client = ollama.Client(
    host="http://host.docker.internal:11434"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

class DocumentProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.document = None
        self.page_text = []
        self.chunks = []
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def open_documents(self):
        self.document = pymupdf.open(self.filename)
        
    def extract_pages(self):
        extracted_text = []

        for page in self.document:
            text = page.get_text()

            if not text.strip():
                pix = page.get_pixmap()
                image = Image.open(
                    BytesIO(pix.tobytes("png"))
                )

                text = self.perform_ocr(image)

            extracted_text.append(text)

        self.page_text = extracted_text

    def perform_ocr(self, image):
        text = pytesseract.image_to_string(image)
        return text

    def chunk_text(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )

        documents = splitter.create_documents(
            self.page_text,
            metadatas=[
                {"page": page_number + 1} for page_number in range(len(self.page_text))
            ]
        )

        self.chunks = documents

        return self.chunks

    def embed_chunks(self):
        texts = [chunk.page_content for chunk in self.chunks]

        embeddings = self.embedding_model.encode(texts)

        return embeddings

    def store_embeddings(self, embeddings):
        collection = client.get_or_create_collection(name="documents")

        documents = [chunk.page_content for chunk in self.chunks]

        metadatas = [chunk.metadata for chunk in self.chunks]

        ids = [f"chunk_{i}" for i in range(len(self.chunks))]

        collection.add(
            ids = ids,
            documents = documents,
            embeddings = embeddings.tolist(),
            metadatas = metadatas
        )

    def retrieve(self, query, n_results=5):
        collection = client.get_collection(name = "documents")

        query_embedding = self.embedding_model.encode([query])

        results = collection.query(query_embeddings = query_embedding.tolist(), n_results = n_results)
                
        return results

    def generate_answer(self, query, context):
        prompt = f"""
        Use the following context to answer the question.

        Context:
        {context}

        Question:
        {query}

        Answer only from the provided context. If the answer is not in the context, say you don't know.
        """
        response = ollama_client.chat(
            model="gpt-oss:20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content

def main():

    doc = DocumentProcessor("test_data/Questioned_documents.pdf")

    doc.open_documents()
    doc.extract_pages()
    doc.chunk_text()

    embeddings = doc.embed_chunks()
    doc.store_embeddings(embeddings)

    ask_ollama(doc)

def ask_ollama(doc):
    while True:
        try:
            query = input("\nHow may I help you?: ")

            if query.lower() in {"exit", "quit"}:
                break

            if not query.strip():
                continue
            
            results = doc.retrieve(query)
            context = "\n\n".join(results["documents"][0])
            answer = doc.generate_answer(query, context)

            print("\n--- Answer ---")
            print(answer)

        except EOFError:
            break
    
if __name__ == "__main__":
    main()