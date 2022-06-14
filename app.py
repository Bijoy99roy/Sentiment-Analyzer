from flask import Flask, request, render_template, redirect, url_for
from preprocessing.data_preprocessing import PreProcessing
from prediction.prediction import Predictor
from database.database import DataBase
from datetime import datetime
from flask_cors import cross_origin

app = Flask(__name__)
db_operator = DataBase()
prediction_result = None
tweet_value = None


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    try:
        db_operator.connect_db()
        if db_operator.is_connected():
            db_operator.create_tables()
        else:
            db_operator.connect_db()
            db_operator.create_tables()

        return render_template('index.html')
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        global tweet_value, prediction_result
        if request.method == 'POST':
            tweet = str(request.form.get('tweet'))
            tweet_value = tweet
        preprocessing_obj = PreProcessing()
        tweet_preprocessed = preprocessing_obj.remove_noises(tweet)
        tweet_preprocessed = preprocessing_obj.join_texts(tweet_preprocessed)
        tweet_vectorized = preprocessing_obj.vectorize_data(tweet_preprocessed)
        predictor = Predictor()
        prediction = predictor.predict(tweet_vectorized)[0]
        prediction_result = prediction
        if prediction == 1:
            sentiment = 'Positive Sentiment'
        else:
            sentiment = 'Negative Sentiment'
        return render_template('result.html', data={'result': sentiment})
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/feedback', methods=['POST'])
@cross_origin()
def save_feedbacks():
    try:

        if request.method == 'POST':
            feedback = request.form['feedback']
        now = datetime.now()
        date = now.date()
        current_time = now.strftime('%H:%M:%S')
        if prediction_result == 1 and feedback == 'Yes':
            sentiment = 'Positive'
        elif prediction_result == 1 and feedback == 'No':
            sentiment = 'Negative'
        elif prediction_result == 0 and feedback == 'Yes':
            sentiment = 'Negative'
        else:
            sentiment = 'Positive'
        db_operator.insert_data('dataset', date, current_time, tweet_value, sentiment)
        return redirect(url_for('home'))
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


if __name__ == "__main__":
    app.run(debug=True)