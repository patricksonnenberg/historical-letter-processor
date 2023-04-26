import spacy
import nltk

from summarizer import Summarizer
# Will need this command: pip install bert-extractive-summarizer
# Might need to import torch as well

nlp = spacy.load("en_core_web_sm")
nltk.download('brown')
brown_words = set(nltk.corpus.brown.words())

def check_validity(string_input):
    """
    This method checks if the generated string of text contains mostly gibberish
    or mostly words found in the Brown corpus. A score is generated and it must
    meet a threshold for it to be considered a "valid" generation.
    """
    tokenized_text = nltk.word_tokenize(string_input)  # Produces list of tokens
    token_count = 0
    valid_tokens = 0
    for token in tokenized_text:
        token_count += 1
        if token.lower() in brown_words:  # Checking if it's a valid word or gibberish
            valid_tokens += 1
    score = valid_tokens / token_count if token_count != 0 else 0
    if score >= 0.7:  # Score must meet a threshold for it to be considered a valid generation
        return True
    else:
        return False

def get_summary(input_string):
    """
    This method utilizes BERT's summarization to summarize the document.
    """
    model = Summarizer()
    return model(input_string, num_sentences=2)
