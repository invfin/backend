import os
from pathlib import Path
import importlib


class CreateTests:
    """
    In this class is where the test files, class and functions are created
    """
    def inspect_django_app_folder(self, app: str):
        """
        Given an app it looks over all the files and folders inside.
        If there isn't a test folder it creates it.
        """
        path = Path(importlib.import_module(app).__file__).parent.resolve()
        for file in os.listdir(path):
            if file.startswith('test'):
                if Path(f'{path}/{file}').is_file():
                    return self.create_tests_folder(path, file)
                else:
                    if '__init__.py' not in os.listdir(f'{path}/{file}'):
                        with open(f'{path}/{file}/__init__.py', 'w') as f:
                            f.close()
                    return f'{path}/{file}'
        return self.create_tests_folder(path)

    def create_tests_folder(self, path: Path, file: bytes = None):
        """
        Creates a test folder with and __init__ file if necessary
        """
        test_folder = f'{path}/tests'
        os.mkdir(test_folder)
        with open(f'{test_folder}/__init__.py', 'w') as f:
            f.close()
        if file:
            os.rename(f'{path}/{file}', f'{test_folder}/{file}')
        return test_folder
