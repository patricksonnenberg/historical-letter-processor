import unittest
from collections import defaultdict
from process_files import PdfDoc, convert_pdf_to_img, ocr, process_file

class TestMyFile(unittest.TestCase):

    def test_file(self, transcript_path, original_path):
        """
        This method compares the OCR results to a manual transcription of
        the file, which we wrote ourselves. We calculate how similar they
        are based on word counts, and if the percentage correct meets a
        certain threshold, it will pass.
        """
        ocr_results = process_file(original_path)[-1]
        ocr_results = ocr_results.rstrip('\n').lower()
        tokenized_ocr = ocr_results.split()
        ocr_dict = defaultdict(int)  # Creating dict for counts
        for token in tokenized_ocr:
            ocr_dict[token] += 1
        with open(transcript_path, 'r') as f:
            transcript = f.read().rstrip('\n').lower()
        tokenized_transcript = transcript.split()
        tokenized_dict = defaultdict(int)
        for token in tokenized_transcript:
            tokenized_dict[token] += 1
        correct_count = 0
        total_count = 0
        for key, value in tokenized_dict.items():  # Comparing counts
            if key in ocr_dict:
                token_count = tokenized_dict[key]
                ocr_count = ocr_dict[key]
                total_count += token_count  # Based off gold transcript
                correct_count += min(token_count, ocr_count)
        percent_similar = correct_count / total_count
        print(percent_similar)
        self.assertTrue(percent_similar >= 0.65)


if __name__ == '__main__':
    originals_paths = ['test_transcripts/originals/9.jpeg', 'test_transcripts/originals/10.jpeg', 
                        'test_transcripts/originals/23.jpeg', 'test_transcripts/originals/41.pdf',
                        'test_transcripts/originals/45.pdf', 'test_transcripts/originals/92.pdf']
    
    transcript_paths = ['test_transcripts/transcripts/9.txt', 'test_transcripts/transcripts/10.txt', 
                        'test_transcripts/transcripts/23.txt', 'test_transcripts/transcripts/41.txt',
                        'test_transcripts/transcripts/45.txt', 'test_transcripts/transcripts/92.txt']
    
    for transcript_path, original_path in zip(transcript_paths, originals_paths):
        test = TestMyFile()
        test.test_file(transcript_path, original_path)
