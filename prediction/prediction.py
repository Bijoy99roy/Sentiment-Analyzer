import os
from utils.all_utils import read_yaml, load_file

class Predictor:
    def __init__(self):
        pass

    def predict(self, data):
        try:
            config = read_yaml(self.config_path)
            artifact_dir = config['ARTIFACTS']['ARTIFACTS_DIR']
            trained_model_file = config['ARTIFACTS']['TRAINED_MODEL']
            trained_model_file_path = os.path.join(artifact_dir, trained_model_file)
            model = load_file(trained_model_file_path)
            predicted_result = model.predict(data)
            return predicted_result
        except FileNotFoundError as fnf:
            print(str(fnf))
        except Exception as e:
            print(str(e))