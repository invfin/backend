import os
from pathlib import Path
import configparser
import sys
import importlib


class ConfigFiles:
    """
    A class to find and/or create configuration files to be able to
    create tests easily in all the local apps installed in the django project.
    """
    current_path = Path(__file__).parent.resolve().parent
    config_parser = configparser.ConfigParser()

    def __init__(self) -> None:
        self.files_to_look_for = {
            "setup.cfg": {"visited": False, "function": self.parse_setup_cfg},
            "pytest.ini": {"visited": False, "function": self.parse_pytest_ini},
        }

    def parse_pytest_ini(self, file_path):
        """
        If a pytest init file is found it looks for the django config files
        to find the settings to know which apps are installed
        """
        self.config_parser.read(file_path)
        sections = self.config_parser.sections()
        if 'pytest' in sections:
            if self.config_parser['pytest']['addopts']:
                possible_config = self.config_parser['pytest']['addopts'].strip()
                if possible_config.startswith('--ds='):
                    possible_config = possible_config.replace('--ds=', '')
                if possible_config.endswith(' --reuse-db'):
                    possible_config = possible_config.replace(' --reuse-db', '')
                return possible_config
            else:
                return self.config_parser['pytest']['python_files']

    def parse_setup_cfg(self, file_path):
        """
        If a setup.cfg file is found it looks for the django config files
        to find the settings to know which apps are installed
        """
        self.config_parser.read(file_path)
        sections = self.config_parser.sections()
        if 'mypy.plugins.django-stubs' in sections:
            if 'django_settings_module' in self.config_parser['mypy.plugins.django-stubs']:
                return self.config_parser['mypy.plugins.django-stubs']['django_settings_module']
        if 'isort' in sections:
            if 'known_first_party' in self.config_parser['isort']:
                return self.config_parser['isort']['known_first_party']

    def find_django_config_file(self):
        """
        It looks over all the directories and files in the root directory
        to find a setup, pytest o manage file to be able to find the settings
        files/directory of the django project to know which apps are installed
        """
        for file in os.listdir(self.current_path):
            if file in self.files_to_look_for.keys():
                if not self.files_to_look_for[file]["visited"]:
                    django_config_file = self.files_to_look_for[file]["function"](file)
                    if django_config_file:
                        return django_config_file
                    self.files_to_look_for[file]["visited"] = True
            continue
    
    def create_config_settings(self, django_settings_module, django_local_apps):
        if not "setup.cfg" in os.listdir(self.current_path):
            with open(f'{self.current_path}/setup.cfg', 'w') as f:
                f.close()
        self.config_parser.read("setup.cfg")
        sections = self.config_parser.sections()
        if not "autotest" in sections:
            self.config_parser["autotest"] = {
                "django_settings_module": django_settings_module,
                "django_local_apps": ",".join(django_local_apps)
            }
            with open('setup.cfg', 'w') as conf:
                self.config_parser.write(conf)
    
    def check_environ(self):
        return os.getenv("DJANGO_SETTINGS_MODULE", default=None)

    @classmethod
    def get_all_django_apps(cls):
        """
        It gets all the apps that the ConfigClass has found
        """
        configuration = cls().check_environ()
        if not configuration:
            configuration = cls().find_django_config_file()
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", configuration)
        sys.path.insert(0, configuration.replace(".", "/"))
        print(sys.modules)
        conf_import = importlib.import_module(configuration)
        

        print(conf_import)
        return apps
