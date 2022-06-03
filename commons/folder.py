import os
import shutil


def create_folders(directory: str):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print(f'Error: Creating directory. {directory}')


def remove_folders(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)