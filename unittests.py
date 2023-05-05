import unittest

import unittest
from pathlib import Path
from unittest.mock import patch, call
from process_files import PdfDoc, convert_pdf_to_img, ocr, process_file
from summarizer import Summarizer

from process_text import check_validity, get_summary, nlp, brown_words

class TestConvertPdfToImg(unittest.TestCase):
    def setUp(self):
        self.pdf_path = Path("test_files/test.pdf")
        self.pdf_doc = PdfDoc(self.pdf_path)

    def test_return_type(self):
        images_list = convert_pdf_to_img(self.pdf_doc)
        self.assertIsInstance(images_list, list)
        self.assertTrue(all(isinstance(i, Path) for i in images_list))


class TestOcr(unittest.TestCase):
    def setUp(self):
        self.images_list = [Path("test_files/test_0.jpg"), Path("test_files/test_1.jpg")]

    def test_return_type(self):
        ocr_text = ocr(self.images_list)
        self.assertIsInstance(ocr_text, str)


class TestProcessFile(unittest.TestCase):
    def setUp(self):
        self.pdf_path = Path("test_files/test.pdf")
        self.jpeg_path = Path("test_files/test.jpeg")
        self.unknown_file = Path("test_files/test.txt")

    def test_pdf_file(self):
        files_list, text = process_file(self.pdf_path)
        self.assertTrue(all(isinstance(f, str) for f in files_list))
        self.assertIsInstance(text, str)

    def test_jpeg_file(self):
        files_list, text = process_file(self.jpeg_path)
        self.assertTrue(all(isinstance(f, str) for f in files_list))
        self.assertIsInstance(text, str)

    def test_unknown_file(self):
        with self.assertRaises(ValueError):
            process_file(self.unknown_file)


class TestGibberishAndSummarizer(unittest.TestCase):
    def test_check_validity(self):
        # Test for input with mostly valid words
        valid_input = "This is a valid input sentence."
        self.assertTrue(check_validity(valid_input))

        # Test for input with mostly gibberish
        gibberish_input = "XoLcAlBpLzEaPdItJgZqHmWnRvUfTsYkN word alefkjblfbf"
        self.assertFalse(check_validity(gibberish_input))

        # Test for input with score below threshold
        invalid_input = "afladfjs is input pllewa some valid words gigjvhhgd mostly gibberish."
        self.assertFalse(check_validity(invalid_input))

    def test_get_summary(self):
        # Test that it returns two sentences
        input_text = """
        Sophie was a young girl who loved playing in her garden. 
        She spent hours each day planting and tending to her flowers. 
        One day, she noticed a small snail slowly making its way across the garden. 
        Sophie decided to build a little house for the snail, using a small box and some leaves. 
        From that day on, Sophie and the snail became great friends, and the snail would visit her garden every day."""
        summary = get_summary(input_text)
        self.assertEqual(summary.count('.'), 2)
        

if __name__ == '__main__':
    unittest.main()

