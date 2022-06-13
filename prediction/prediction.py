import os
from utils.all_utils import read_yaml, load_file
from flask import render_template

class Predictor:
    def __init__(self):
        self.config_path = 'config/config.yaml'

    def predict(self, data):
        """
        This method predicts if a sentence if Negative or Positive
        :param data: 2d matrix
        :return: 1d result array
        """
        try:
            config = read_yaml(self.config_path)
            artifact_dir = config['ARTIFACTS']['ARTIFACTS_DIR']
            trained_model_file = config['ARTIFACTS']['TRAINED_MODEL']
            trained_model_file_path = os.path.join(artifact_dir, trained_model_file)
            model = load_file(trained_model_file_path)
            predicted_result = model.predict(data)
            return predicted_result
        except FileNotFoundError as fnf:
            message = 'Error :: ' + str(fnf)
            return render_template('exception.html', exception=message)
        except Exception as e:
            message = 'Error :: ' + str(e)
            return render_template('exception.html', exception=message)