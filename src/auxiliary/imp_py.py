# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="rasmadeus"
__date__ ="$16.10.2014 21:43:57$"


def get_imported_py_modules(start_path, except_starts_with=()):
    
    def is_good_file_name(file_name, except_starts_with):
        lower_file_name = file_name.lower()
        return \
            lower_file_name.startswith(except_starts_with) == False and\
            lower_file_name.endswith('.py') == True            

    import os
    import importlib
    
    modules = []
    for dir_path, _, file_names in os.walk(start_path):
        for file_name in file_names:
            if is_good_file_name(file_name, except_starts_with):
                path_to_module = '.'.join([dir_path, file_name.split('.')[0]])
                path_to_module = path_to_module[2:].replace('\\','.')
                modules.append(importlib.import_module(path_to_module))
    return modules