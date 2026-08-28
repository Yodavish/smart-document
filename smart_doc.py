import pymupdf
import pytesseract
from io import BytesIO
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def main():

    doc = pymupdf.open("test_data/spytm_Scanned.pdf")
    page = doc[0]
    pix = page.get_pixmap()
    image = Image.open(BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(image)
    print(text)

if __name__ == "__main__":
    main()