import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
