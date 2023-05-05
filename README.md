## Historical Letter Processor

This project began as a way to read in ancestral historical letters, though it can apply boradly to any letter or PDF. It can be used as a tool to document fmaily history. The letter processor allows a user to upload a PDF or jpeg of a letter, where the text is automatically recognized and extracted. The user can then update the text if it is incorrect, and once they're satisfied, it will be stored in a backend database. In addition, a summary of the letter is generated, along with all of the entities found in the document. They can access all the documents they have stored, and continue to access those summaries and entities, as they are all stored in the database. 

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
We ran into a few challenges, especially with tesseract, as it seemed to be working slightly different with Macs and PCs. 

### Table of Contents


### Modules and Versions

conda 4.14.0

conda-build 3.21.5

flask 2.2.2

python 3.9.7

spacy 3.3.1

werkzeug

pillow

pdf2image

python-poppler

nltk

bert-extractive-summarizer

torch

tesseract
    <br>--macOS: brew install tesseract
