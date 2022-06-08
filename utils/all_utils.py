import yaml
import pickle

def read_yaml(path_to_yaml):
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content
    except Exception as e:
        print(str(e))


def load_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError as fnf:
        print(str(fnf))
    except Exception as e:
        print(str(e))