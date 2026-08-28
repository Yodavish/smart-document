import pymupdf
import pytesseract
from io import BytesIO
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def main():
    pages = open_documents("test_data/spytm_Scanned.pdf")
    text = extract_pages(pages)
    save_text(text)

def open_documents(filepath):
    return pymupdf.open(filepath)
       
def extract_pages(pages):
    extracted_text = []

    for page in pages:
        text = page.get_text()

        if not text.strip():
            pix = page.get_pixmap()
            image = Image.open(BytesIO(pix.tobytes("png")))

            text = perform_ocr(image)

        extracted_text.append(text)

    return extracted_text

def perform_ocr(image):
    return pytesseract.image_to_string(image)

def save_text(text):
    with open("output/result.txt", "a") as file:
        file.write("\n\n".join(text))

if __name__ == "__main__":
    main()