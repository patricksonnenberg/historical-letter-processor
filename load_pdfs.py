import fitz
from pdf2image import convert_from_path
from pathlib import Path
import argparse
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



def convert_pdf_to_img(doc: PdfDoc, images_file_path: Path):
    if doc.pdf_type == "scanned_pdf":
        pdf_path = doc.pdf_file_path
        pdf_dir = images_file_path.joinpath(pdf_path.stem)
        pdf_dir.mkdir(parents=True, exist_ok=True)
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image_path = pdf_dir.joinpath(f"{pdf_path.stem}_{i}.jpg")
            image.save(image_path)
        print(f"completed converting pdf file '{pdf_path.stem}' to jpg(s)")
    else:
        raise ValueError(f"Digital pdf file '{doc.pdf_file_path.stem}' doesn't need to be converted")



def main():
    parser = argparse.ArgumentParser(description="Loads PDF files and analyzes contents")
    parser.add_argument('--pdf_folder', type=str, help='Folder containing the PDF files', required=True)
    parser.add_argument('--images_folder', type=str, help='Folder to save the JPG images that have been converted from PDFs', required=True)
    args = parser.parse_args()
    
    input_pdf_folder = Path(args.pdf_folder)
    output_jpg_folder = Path(args.images_folder)
    
    pdf_files = [f for f in os.listdir(input_pdf_folder) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = input_pdf_folder.joinpath(pdf_file)
        pdf_obj = PdfDoc(pdf_path)
        if pdf_obj.pdf_type == "scanned_pdf":
            print(f"pdf file '{pdf_obj.pdf_file_path.stem}' is a scanned pdf")
            convert_pdf_to_img(doc=pdf_obj, images_file_path=output_jpg_folder)
        else:
            print(f"pdf file '{pdf_obj.pdf_file_path.stem}' is a digital pdf")

if __name__ == "__main__":
    main()
    