FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app
RUN pip install flask spacy && \
    python -m spacy download en_core_web_sm
RUN apt-get update && apt-get install -y tesseract-ocr poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"
EXPOSE 5000
CMD ["python", "process_letters.py"]