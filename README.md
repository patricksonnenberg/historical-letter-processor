## Historical Letter Processor

This project began as a way to read in ancestral historical letters, though it can apply broadly to any letter or PDF. It can be used as a tool to document family history. The letter processor allows a user to upload a PDF or jpeg of a letter, where the text is automatically recognized and extracted. The user can then update the text if it is incorrect, and once they are satisfied, it will be stored in a backend database. In addition, a summary of the letter is generated, along with all of the entities found in the document. They can access all the documents they have stored, and continue to access those summaries and entities, as they are all stored in the database. 

As a quick note, building the docker image might take a couple minutes, as might the OCR, especially on the first run. 

### Flask Webserver
This project uses a flask webserver that allows a user to upload their historical letter. The letter's text is processed using tesseract and OCR. The summarization is generated using BERT's summarizer tool, and the entities are extracted with spaCy's NER processing. 

##### To run (without Docker): 
Run the process_letters.py file:
```bash
python process_letters.py
```
Go to the address (http://127.0.0.1:5000).

##### To run (with Docker): 
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
We ran into a few challenges, especially with tesseract, as it seemed to be working slightly different with Macs and PCs. The Docker image, however, solved this issue for us. 

### Table of Contents

templates folder - HTML file templates to generate the webpages

db.py - handles the backend database storage and access

Dockerfile - used to create the Docker image

ner.py - handles getting the named entities through spaCy

process_files.py - handles file proccessing, converting PDFs to image, and extracts text

process_letters.py - the main file which handles all the get and post requests

proccess_text.py - checks that the generated text contains too much gibberish and gets the BERT summary

requirements.txt - all the requirements that need to be downloaded, which is handled automatically in the Dockerfile. 

### Modules and Versions
These requirements are found in requirements.txt, which is run when the Docker image is created.

flask==2.2.2
spacy==3.5.0
pytesseract==0.3.10 
werkzeug==2.2.3
pillow==9.4.0
pdf2image==1.16.3
pymupdf==1.22.1
nltk==3.8.1
bert-extractive-summarizer==0.10.1
torch==2.0.0

The rest is handled in the Dockerfile itself, and this includes:

spacy's en_core_web_sm
tesseract-ocr
poppler-utils
nltk's 'punkt'
