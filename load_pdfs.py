import fitz
from pdf2image import convert_from_path
from pathlib import Path

file_path = Path("data/scanned/174.pdf")
images_folder = Path("jpgs_from_pdfs")


class PdfDoc:
    """A class for reading and processing PDF files"""

    def __init__(self, pdf_file_path: Path):
        """
        Initialize as PDFLetter object
        :param input_pdf: The path to the PDF file to read
        """
        self.pdf_file_path = pdf_file_path
        self.doc = fitz.Document()
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

pdf_obj = PdfDoc(file_path)

def convert_pdf_to_img(doc: PdfDoc, images_file_path: Path):
    if doc.pdf_type == "scanned_pdf":
        pdf_path = doc.pdf_file_path
        pdf_dir = images_file_path.joinpath(pdf_path.stem)
        pdf_dir.mkdir(parents=True, exist_ok=True)
        images = convert_from_path(pdf_path)
        i = 0
        for image in images:
            image_path = pdf_dir.joinpath(f"page_{i}.jpg")
            image.save(image_path)
            i += 1
        print(f"Converted {i} pages of pdf '{pdf_path.stem}' to images")
    else:
        raise ValueError(f"Digital pdf '{doc.pdf_file_path.stem}' doesn't need to be converted")

convert_pdf_to_img(doc=pdf_obj, images_file_path=images_folder)