import os
from pathlib import Path
import configparser
import importlib


class ConfigFiles:
    """
    A class to find and/or create configuration files to be able to
    create tests easily in all the local apps installed in the django project.
    """
    current_path = Path(__file__).parent.resolve()
    config_parser = configparser.ConfigParser()

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
        django_config_file = None
        for file in os.listdir(self.current_path):
            if file == 'setup.cfg':
                django_config_file = self.parse_setup_cfg(file)
            elif file == 'pytest.ini':
                django_config_file = self.parse_pytest_ini(file)
            if django_config_file:
                return django_config_file
            continue
        assert "No config files found"

    @classmethod
    def get_all_apps(cls):
        """
        It gets all the apps that the ConfigClass has found
        """
        configuration = cls().find_django_config_file()
        conf_import = importlib.import_module(configuration)
        return conf_import.LOCAL_APPS
