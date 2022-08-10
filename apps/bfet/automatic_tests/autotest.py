from .create_tests import CreateTests
from .settings import ConfigFiles

class Autotest(ConfigFiles, CreateTests):
    @classmethod
    def start(cls, folder_path:str=None, app:str=None):
        cls().create_test_file(
            cls().inspect_folder_for_tests(
                **{"folder_path": folder_path, "app": app}
            )
        )
