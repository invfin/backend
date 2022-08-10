from typing import List, Dict, Callable
import os
from pathlib import Path
import importlib
import importlib.util
import sys
import inspect
from jinja2 import Environment, FileSystemLoader


class CreateTests:
    """
    In this class is where the test files, class and functions are created
    """
    def inspect_folder_for_tests(self, folder_path:str=None, app:str=None) -> Dict:
        """
        Given an folder's path it looks over all the files and folders inside.
        If there isn't a test folder it creates it. If it finds any test file it will
        move it into the tests folder.

        In case of using it with django it also accepts an app.

        Use either folder_path or app. In case of using both, the folder_path will be used.
        """
        test_info = {}
        if app:
            path = Path(importlib.import_module(app).__file__).parent.resolve()
            test_info.update({"app_name": app})
        if folder_path:
            path = folder_path
        if not folder_path and not app:
            path = os.getcwd()
        
        test_info.update({"module_path": path, "files_to_test": []})
        for file in os.listdir(path):
            file_name = file.split(".")[0]
            if file_name in self.files_to_include:
                test_info["files_to_test"].append(file_name)
            if file.startswith('test'):
                if Path(f'{path}/{file}').is_file():
                    test_folder_path = self.create_tests_folder(path, file)
                else:
                    if '__init__.py' not in os.listdir(f'{path}/{file}'):
                        with open(f'{path}/{file}/__init__.py', 'w') as f:
                            f.close()
                    test_folder_path = f'{path}/{file}'
        test_folder_path = self.create_tests_folder(path)
        test_info.update({"test_folder_path": test_folder_path})
        return test_info

    def create_tests_folder(self, path:Path, file:bytes=None) -> str:
        """
        Creates a test folder with and __init__ file
        If there is a file named test alone it moves it to the new tests dir
        """
        test_folder = f'{path}/tests'
        if not os.path.exists(test_folder):
            os.mkdir(test_folder)
            with open(f'{test_folder}/__init__.py', 'w') as f:
                f.close()
        if file:
            os.rename(f'{path}/{file}', f'{test_folder}/{file}')
        return test_folder
    
    def get_class_in_file(self, module_name:str) -> List:
        return inspect.getmembers(
            sys.modules[module_name], 
            lambda member: inspect.isclass(member) and member.__module__ == module_name
        )
    
    def get_class_methods(self, clase):
        """
        We get all the methods of a class, excluding the built-ins and the inheritated
        """
        list_methods = []
        methods = inspect.getmembers(clase, predicate=inspect.isroutine)
        for method in methods:
            if (self.get_class_that_defined_method(method[1]) == clase):
                list_methods.append(method)
        return list_methods
    
    def get_class_that_defined_method(self, method:Callable):
        """
        We retrieve the real class that owns the method
        """
        if inspect.ismethod(method):
            for cls in inspect.getmro(method.__self__.__class__):
                if method.__name__ in cls.__dict__:
                    return cls
            method = method.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(method):
            cls = getattr(inspect.getmodule(method),
                        method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                        None)
            if isinstance(cls, type):
                return cls
    
    def create_test_content(self, module_name:str, file_testing:str):
        env = Environment(loader=FileSystemLoader(f'{self.apps_folder}/templates'))
        file_name = "base" # For the moment we will only use base.py
        template = env.get_template(f"{file_name}.py")
        template_data = {
            "base_app_name": module_name.split(".")[1],
            "app_name": module_name.replace(file_testing, "")[:-1],
            "file_name": file_testing,
            "clases": [],
            "imports": []
        }
        clases = self.get_class_in_file(module_name)
        for clase in clases:
            template_data["imports"].append(clase[0])
            methods = self.get_class_methods(clase[1])
            class_naming = self.class_naming.replace("*", clase[0])
            clase_dict = {"class_naming": class_naming, "functions": []}
            for method in methods:
                function_namig = self.function_namig.replace("*", method[0])
                clase_dict["functions"].append({"function_namig": function_namig})
            template_data["clases"].append(clase_dict)
        return template.render(**template_data)
    
    def create_test_file(self, tests_info:dict):
        # the module_name should be created differently. I should check the actual module name
        app_name = tests_info["app_name"]
        for file in tests_info["files_to_test"]:
            test_file_name = self.file_namig.replace("*", file)
            if not os.path.exists(f'{tests_info["test_folder_path"]}/{test_file_name}.py'):
                module_name = f"{app_name}.{file}"                
                output_from_parsed_template = self.create_test_content(module_name, file)
                with open(f'{tests_info["test_folder_path"]}/{test_file_name}.py', 'w') as f:
                    f.write(output_from_parsed_template)
                    f.close()
