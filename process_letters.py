from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import spacy

from load_pdfs import process_pdf_file
import ner
import db
from werkzeug.utils  import secure_filename
import os

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
connection = db.DatabaseConnection('entities.sqlite')
my_markup_dict = {'mark': "Please return to the home page to add your input."}

IMAGE_DIR = os.path.join('static', 'uploads')
os.makedirs(IMAGE_DIR, exist_ok = True)
app.config['UPLOADED_DOCS'] = IMAGE_DIR


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        # Delete the file if this it has been canceled
        file = request.args.get('file')
        os.remove(file)
    return render_template('home_page.html')


@app.route('/ocr_results', methods=['POST'])
def ocr_results():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOADED_DOCS'], filename))
        img = os.path.join(app.config['UPLOADED_DOCS'], filename)
    else:
        img = ""
    print(img)
    ## get text from pdf/jpeg
    ## show image and a text box for editting the text we find
    found_text = process_pdf_file(img)
    # FROM MELISSA: connected load_pdfs.py functionality to file to make it modular! :)
    return render_template('ocr_results.html', found_text=found_text, image_file=img)

@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

@app.route('/analyze', methods=["GET", "POST"])
def show_result():
    if request.method == "POST":
        text = request.form["doc_text"]
        if text:
            doc = nlp(text)
            spacyed_text = ner.SpacyDocument(text)  # Creating spacy object
            ner_spacyed_text = spacyed_text.get_entities_with_markup()  # Calling on this method in ner to NER-ize the text

            # Iterating over the entities in the doc and update the counts in the database
            cursor = connection.get_cursor()
            for ent in doc.ents:
                # Checking if the entity is already in the database
                cursor.execute("SELECT count FROM entities WHERE label = ? AND text = ?", (ent.label_, ent.text))
                row = cursor.fetchone()
                if row is None:
                    # Inserting a new row for the entity if it doesn't already exist
                    cursor.execute("INSERT INTO entities (label, text, count) VALUES (?, ?, 1)", (ent.label_, ent.text))
                else:
                    # Updating count for the entity if it already exists in the database
                    count = row[0] + 1
                    cursor.execute("UPDATE entities SET count = ? WHERE label = ? AND text = ?", (count, ent.label_, ent.text))
            connection.commit()
            my_markup_dict['mark'] = ner_spacyed_text
            return render_template("result.html", text=ner_spacyed_text, entities=doc.ents)
        else:
            return render_template('result.html', text=my_markup_dict['mark'])  # To prompt user to add input
    else:
        return render_template('result.html', text=my_markup_dict['mark'])  # To prompt user to add input

@app.route('/entity_db')
def get_counts():
    entity_counts = connection.get_entity_counts()
    return render_template("entity_db.html", entity_counts=entity_counts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # So that it can run with docker
