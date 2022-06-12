from flask import Flask, request, render_template
from preprocessing.data_preprocessing import PreProcessing
from prediction.prediction import Predictor


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            tweet = str(request.form.get('tweet'))
        preprocessing_obj = PreProcessing()
        tweet_preprocessed = preprocessing_obj.remove_noises(tweet)
        tweet_preprocessed = preprocessing_obj.join_texts(tweet_preprocessed)
        tweet_vectorized = preprocessing_obj.vectorize_data(tweet_preprocessed)
        predictor = Predictor()
        prediction = predictor.predict(tweet_vectorized)[0]
        if prediction == 1:
            sentiment = 'Positive Sentiment'
        else:
            sentiment = 'Negative Sentiment'
        return render_template('result.html', data={'result': sentiment})
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


if __name__ == "__main__":
    app.run(debug=True)