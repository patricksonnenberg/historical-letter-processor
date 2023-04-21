FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app
RUN pip install flask spacy && \
    python -m spacy download en_core_web_sm
EXPOSE 5000
CMD ["python", "flask_webserver.py"]