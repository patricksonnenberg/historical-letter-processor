from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import spacy

from process_files import process_file
import ner
import db
from werkzeug.utils import secure_filename
import os
import process_text

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
#connection = db.DatabaseConnection('entities.sqlite')
docs_db = db.create_db("historical_docs")
my_markup_dict = {'mark': "Please return to the home page to add your input."}

IMAGE_DIR = os.path.join('static', 'uploads')
os.makedirs(IMAGE_DIR, exist_ok = True)
app.config['UPLOADED_DOCS'] = IMAGE_DIR


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        # Delete the file if this it has been canceled
        files = request.args.get('files')
        for file in files:
            os.remove(file)
    return render_template('home_page.html')

@app.route('/ocr_results', methods=['POST'])
def ocr_results():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOADED_DOCS'], filename))
        original_filename = os.path.join(app.config['UPLOADED_DOCS'], filename)
    else:
        original_filename = ""
    print(original_filename)
    ## get text from pdf/jpeg
    ## show image and a text box for editting the text we find
    img, found_text = process_file(original_filename)
    print(img)
    images = [os.path.join(app.config['UPLOADED_DOCS'], i.split("/")[-1]) for i in img]
    print(images)
    # FROM MELISSA: connected file_loader.py functionality to file to make it modular! :)

    is_valid_text = process_text.check_validity(found_text) # Returns boolean of true or false

    return render_template('ocr_results.html', 
                           found_text=found_text, 
                           image_files=images, 
                           is_valid_text=is_valid_text, 
                           original_filename=original_filename)

@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

@app.route('/analyze', methods=["GET", "POST"])
def show_result():
    # I think once we are here, perhaps we should delete the images to clean up
    if request.method == "POST":
        text = request.form["doc_text"]
        original_filename = request.args.get('original_filename')
        if text:
            doc = nlp(text)
            spacyed_text = ner.SpacyDocument(text)  # Creating spacy object
            ner_spacyed_text = spacyed_text.get_entities_with_markup()  # Calling on this method in ner to NER-ize the text

            summarized_text = process_text.get_summary(text)  # Gets the summary of the text

            docs_db.add_document(original_filename, text, summarized_text)
            # Iterating over the entities in the doc and add to the database
            [docs_db.add_entity(original_filename, ent_text, label) for start, end, label, ent_text in spacyed_text.get_entities()]
            my_markup_dict['mark'] = ner_spacyed_text
        return render_template("summary_ner.html", 
                               text=my_markup_dict['mark'], 
                               entities=doc.ents, 
                               summary=summarized_text, 
                               original_filename=original_filename)
    else:
        return render_template('summary_ner.html', text=my_markup_dict['mark'])  # To prompt user to add input

@app.route('/entity_db')
def get_entity_db():
    original_filename = request.args.get('original_filename')
    if original_filename:
        entities = docs_db.get_entities_by_doc(original_filename)
    else:
        # May want to add some preprocessing to make this a useful page
        entities = docs_db.get_all_entities()
    return render_template("entity_db.html", entities=entities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # So that it can run with docker
