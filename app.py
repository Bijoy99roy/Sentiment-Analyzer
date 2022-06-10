import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from preprocessing.data_preprocessing import PreProcessing
from prediction.prediction import Predictor


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home(is_predicted=False, result=None):
    try:
        return render_template('index.html', data={})
    except Exception as e:
        print(str(e))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            tweet = request.form.get('tweet')
            print(tweet)
        preprocessing_obj = PreProcessing()
        tweet = np.asarray([tweet])
        tweet_tokens = preprocessing_obj.get_tokens(tweet)
        tweet_preprocessed = preprocessing_obj.remove_noises(tweet_tokens)
        tweet_preprocessed = preprocessing_obj.join_texts(tweet_preprocessed)
        tweet_vectorized = preprocessing_obj.vectorize_data(tweet_preprocessed)
        predictor = Predictor()
        prediction = predictor.predict(tweet_vectorized)
        return redirect(url_for('home', is_predicted=True, result=prediction))
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    app.run(debug=True)