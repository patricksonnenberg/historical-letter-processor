## Historical Letter Processor

This assignment... EXPAND MORE HERE

### Flask Webserver
This webserver allows a user to... EXPAND MORE HERE

Upload pdf
Update text
Access the named entities
Access the summarization
See a timeline

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

### Modules and Versions

conda 4.14.0

conda-build 3.21.5

flask 2.2.2

python 3.9.7

spacy 3.3.1

tesseract

ADD MORE MODULES HERE