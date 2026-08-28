import pymupdf
import pytesseract
from io import BytesIO
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

class DocumentProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.document = None
        self.page_text = []
        self.chunks = []

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
        return pytesseract.image_to_string(image)

    def chunk_page(self, chunk_page_size = 5):
        for i in range(0, len(self.page_text), chunk_page_size):
            self.chunks.append(self.page_text[i:i + chunk_page_size])

        return self.chunks

def main():
    doc = DocumentProcessor("test_data/Questioned_documents.pdf")

    doc.open_documents()
    doc.extract_pages()
    doc.chunk_page()

    print(f"Pages: {len(doc.page_text)}")
    print(f"Chunks: {len(doc.chunks)}")


if __name__ == "__main__":
    main()