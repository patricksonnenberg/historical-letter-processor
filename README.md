## Historical Letter Processor

This project began as a way to read in ancestral historical letters, though it can apply broadly to any letter or PDF. It can be used as a tool to document family history. The letter processor allows a user to upload a letter of file type PDF or JPEG, where the text is automatically recognized and extracted. The user can then update the text if it is incorrect, and once they are satisfied, it will be stored in a backend database. In addition, a summary of the letter is generated, along with all of the entities found in the document. They can access all the documents they have stored, and continue to access those summaries and entities, as they are all stored in the database. 

As a quick note, building the docker image might take a couple minutes, as might the OCR and summarizing, especially on the first run. 

### Flask Webserver

This project uses a flask webserver that allows a user to upload their historical letter. The letter's text is processed using tesseract and OCR. The summarization is generated using BERT's summarizer tool, and the entities are extracted with spaCy's NER processing. 

### To run (without Docker): 
Note: Tesseract and Poppler will need to be installed as well as all packages in requirements.txt.

Run the process_letters.py file:
```bash
python process_letters.py
```
Go to the address (http://127.0.0.1:5000).

### To run (with Docker): 

Create the Docker image by first navigating to the folder in the terminal and running the command:
```bash
docker build -t historicalletterapp .
```

This builds a Docker image called historicalletterapp. Now run this command to start a container from this image:
```bash
docker run -p 5000:5000 historicalletterapp
```

This maps port 5000 in the container to port 5000 on the host machine. Now go to http://localhost:5000 or http://127.0.0.1:5000 in a web browser to see the app. 

To stop the container, manually stop it in the Docker app, or run the command:
```bash
docker ps
```

This will provide the name of the container, which can then be used in the command:
```bash
docker stop <name>
```

### Challenges

We ran into a few challenges, especially with tesseract, as it seemed to be working slightly different with Macs and PCs. The Docker image, however, solved this issue for us. We also ran into some formatting issues with the HTML files, but were able to figure it out. 

### Testing

We have created simple unit tests that are found in unittests.py. There's also test_accuracy.py, which does a qualitative test of the transcripts. We hand-transcribed six transcripts and compared those to the OCR output, generating a similarity score. As the transcripts were personal, we have decided to not include them in this repository, but can share them upon request. 

If you wish to run either one of these tests, they would need to be run outside of the Docker file. 

### Table of Contents

templates folder - HTML file templates to generate the webpages

db.py - handles the backend database storage and access

Dockerfile - used to create the Docker image

ner.py - handles getting the named entities through spaCy

process_files.py - handles file proccessing, converting PDFs to image, and extracts text

process_letters.py - the main file which handles all the get and post requests

proccess_text.py - checks that the generated text contains too much gibberish and gets the BERT summary

requirements.txt - all the requirements that need to be downloaded, which is handled automatically in the Dockerfile. 

test_accuracy.py - performs qualitative test of gold transcripts (transcripts not provided)

unittests.py - performs unit tests to ensure methods are functioning properly

### Modules and Versions

These requirements are found in requirements.txt, which is run when the Docker image is created.

flask==2.2.2 - for building web application

spacy==3.5.0 - for NER processing

pytesseract==0.3.10 - for OCR, python wrapper for tesseract

werkzeug==2.2.3 - for loading files

pillow==9.4.0 - for creating pillow image objects to be read by OCR

pdf2image==1.16.3 - for converting PDF to image

pymupdf==1.22.1 - for extracting text from a PDF that has searchable text

nltk==3.8.1 - for tokenization and text processing

bert-extractive-summarizer==0.10.1 - to summarize the text

torch==2.0.0 - for BERT summarizer

The rest is handled in the Dockerfile itself, and this includes:

spacy's en_core_web_sm - for spacy 

tesseract-ocr - for OCR

poppler-utils - for PDF to image conversion

nltk's 'punkt' - for NLTK
