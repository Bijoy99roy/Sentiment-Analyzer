import yaml
import pickle
from flask import render_template


def read_yaml(path_to_yaml):
    """
    This method helps in reading an yaml file
    :param path_to_yaml: path of yaml file to be read
    :return: yaml content dictionary
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


def load_file(file_path):
    """
    This method helps in loading the serialized files
    :param file_path: path to the serialized files
    :return: Deserialized file object
    """
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError as fnf:
        message = 'Error :: ' + str(fnf)
        return render_template('exception.html', exception=message)
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)