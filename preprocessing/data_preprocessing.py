import re
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.all_utils import read_yaml, load_file


class PreProcessing:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.config_path = 'config/config.yaml'

    def get_tokens(self, tweets):
        try:
            generated_tokens = []
            for tweet in tweets:
                doc = self.nlp(tweet)
                for sent in doc.sents:
                    tokens = []
                    for token in sent:
                        tokens.append(token)
                    generated_tokens.append(tokens)
            return generated_tokens
        except ValueError as ve:
            print(str(ve))
        except Exception as e:
            print(str(e))

    def remove_noises(self, tweet_tokens, stop_words=()):
        try:
            cleaned_tokens = []
            for token in tweet_tokens:
                if token.pos_ in ['PROUN', 'ADJ', 'NOUN', 'VERB']:
                    token = token.lemma_
                    token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
                    token = re.sub("(@[A-Za-z0-9_]+)", "", token)

                    if len(token) > 0 and token not in punctuation and token.lower() not in stop_words:
                        cleaned_tokens.append(token.lower())
            return cleaned_tokens
        except Exception as e:
            print(str(e))

    def join_texts(self, tokens):
        try:
            return " ".join(tokens)
        except Exception as e:
            print(str(e))

    def vectorize_data(self, data):
        try:
            config = read_yaml(self.config_path)
            artifact_dir = config['ARTIFACTS']['ARTIFACTS_DIR']
            vectorizer_file = config['ARTIFACTS']['VECTORIZER']
            vectorizer_path = os.path.join(artifact_dir, vectorizer_file)
            vectorizer = load_file(vectorizer_path)
            transformed_data = vectorizer.transform(data)
            return transformed_data
        except Exception as e:
            print(str(e))
