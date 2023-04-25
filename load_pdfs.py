import platform
import urllib.request
import fitz
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path
from pytesseract import pytesseract
import os


class PdfDoc:
    """A class for reading and processing PDF files"""

    def __init__(self, pdf_file_path: Path):
        """
        Initialize as PDFLetter object
        :param input_pdf: The path to the PDF file to read
        """
        self.pdf_file_path = pdf_file_path
        self.doc = fitz.Document(pdf_file_path)
        self.pdf_text = self.extract_text()
        self.pdf_type = "scanned_pdf" if len(self.pdf_text) == 0 else "digital_pdf"

    def extract_text(self) -> str:
        """
        Extract text from all pages of the PDF.
        :return: The extracted text.
        """
        return ''.join(page.get_textpage().extractText() for page in self.doc)

    def __str__(self):
        return f"PdfDoc object for file '{self.pdf_file_path.name}'"


def convert_pdf_to_img(doc: PdfDoc) -> list[Image]:
    if doc.pdf_type == "scanned_pdf":
        return convert_from_path(doc.pdf_file_path, dpi=300)
    else:
        raise ValueError(f"Digital pdf file '{doc.pdf_file_path.stem}' doesn't need to be converted")

def ocr(image_list: list[bytes]) -> str:
    text_pages = []
    for image in image_list:
        text = pytesseract.image_to_string(image)
        text = text.replace("-\n", "")
        text_pages.append(text)
    return "\n".join(text_pages)

def process_pdf_file(file_path: str):
    pdf_file_path = Path(f"UPLOADED_DOCS/{file_path}")
    pdf_obj = PdfDoc(pdf_file_path)
    if pdf_obj.pdf_type == "scanned_pdf":
        print(f"PDF file '{pdf_obj.pdf_file_path.stem}' is a scanned PDF. Converting to JPEG file and processing text through OCR...")
        image_bytes = convert_pdf_to_img(doc=pdf_obj)
        return ocr(image_bytes)
    else:
        print(f"PDF file '{pdf_obj.pdf_file_path.stem}' is a digital PDF.")
        return pdf_obj.pdf_text


if __name__ == "__main__":
    # check the operating system
    os_name = platform.system()
    if os_name == 'Linux' or os_name == 'Darwin':  # for Unix-based systems like Linux and macOS
        # check if tesseract is installed
        try:
            os.system('which tesseract')
        except OSError:
            raise Exception(
                'tesseract is not installed. Please run "sudo apt-get install tesseract-ocr" for Linux or "brew install tesseract" for macOS')
    else:  # for Windows
        # set up the Tesseract download URL and filename
        url = 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe'
        filename = 'tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe'
        # download Tesseract if it's not installed
        if not os.path.exists(filename):
            urllib.request.urlretrieve(url, filename)
        # set tesseract_cmd path
        tesseract_cmd = os.path.join(os.getcwd(), 'tesseract', 'tesseract.exe')
        pytesseract.tesseract_cmd = tesseract_cmd
    