import re
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.all_utils import read_yaml, load_file
from flask import render_template


class PreProcessing:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.config_path = 'config/config.yaml'

    def remove_noises(self, tweet_tokens, stop_words=STOP_WORDS):
        """
        This method removes noises from the text
        :param tweet_tokens: word token created by spacy
        :param stop_words: Mostly occuring words that are not required for training
        :return: cleaned_token: Preprocessed tokens
        """
        try:
            cleaned_tokens = []
            tweet_tokens = self.nlp(tweet_tokens)
            for token in tweet_tokens:
                if token.pos_ in ['PROUN', 'ADJ', 'NOUN', 'VERB']:
                    token = token.lemma_
                    token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
                    token = re.sub("(@[A-Za-z0-9_]+)", "", token)

                    if len(token) > 0 and token not in punctuation and token.lower() not in stop_words:
                        cleaned_tokens.append(token.lower())
            return cleaned_tokens
        except Exception as e:
            message = 'Error :: ' + str(e)
            return render_template('exception.html', exception=message)

    def join_texts(self, tokens):
        """
        This method joins the tokens into a single sentence
        :param tokens: list of tokens
        :return:
        """
        try:
            return [" ".join(tokens)]
        except Exception as e:
            message = 'Error :: ' + str(e)
            return render_template('exception.html', exception=message)

    def vectorize_data(self, data):
        """
        This method vectorizes the sentences
        :param data: 2d matrix of sentences
        :return: 2d vector matrix
        """
        try:
            config = read_yaml(self.config_path)
            artifact_dir = config['ARTIFACTS']['ARTIFACTS_DIR']
            vectorizer_file = config['ARTIFACTS']['VECTORIZER']
            vectorizer_path = os.path.join(artifact_dir, vectorizer_file)
            vectorizer = load_file(vectorizer_path)
            transformed_data = vectorizer.transform(data)
            return transformed_data
        except Exception as e:
            message = 'Error :: ' + str(e)
            return render_template('exception.html', exception=message)
