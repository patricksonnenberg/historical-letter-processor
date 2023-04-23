from flask import Flask, request, render_template, redirect, url_for
import spacy
import ner
import db
from werkzeug.utils  import secure_filename
import os

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
connection = db.DatabaseConnection('entities.sqlite')
my_markup_dict = {'mark': "Please return to the home page to add your input."}

IMAGE_DIR = "templates/UPLOADED_DOCS/"
os.makedirs(IMAGE_DIR, exist_ok = True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            dir_file_name = IMAGE_DIR + uploaded_file.filename
            uploaded_file.save(dir_file_name)
        return redirect(url_for('show_result', file=dir_file_name))
    return render_template('home_page.html')


@app.route('/analyze', methods=["GET", "POST"])
def show_result():
    file = request.args.get('file')
    print(file)
    ## get text from pdf/jpeg
    # this may need to be split into multiple methods
    ## show image and a text box for editting the text we find
    if request.method == "POST":
        text = request.form["text_input"]
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
            return render_template("result.html", text=ner_spacyed_text, entities=doc.ents, imgage_file=file)
        else:
            return render_template('result.html', text=my_markup_dict['mark'], imgage_file=file)  # To prompt user to add input
    else:
        return render_template('result.html', text=my_markup_dict['mark'], imgage_file=file)  # To prompt user to add input

@app.route('/entity_db')
def get_counts():
    entity_counts = connection.get_entity_counts()
    return render_template("entity_db.html", entity_counts=entity_counts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # So that it can run with docker
