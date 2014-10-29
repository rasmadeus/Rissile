# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="rasmadeus"
__date__ ="$16.10.2014 21:43:57$"

def create_path_to_module(current_dir_path, file_name):
    path_to_module = '.'.join([current_dir_path, file_name.split('.')[0]])
    return  path_to_module[2:].replace('\\','.')


def import_module(path_to_module, modules):
    import importlib
    try:
        module = importlib.import_module(path_to_module)
        modules.append(module)
    except:
        pass

    
def get_all_imported_modules(start_path, pattern='\S+\.py'):
    def is_file_desired(file_name, pattern):
        import re
        try:
            return re.compile(pattern).match(file_name) != None
        except:
            return False
    
    import os
    
    modules = []
    for current_dir_path, dirs_name, files_name in os.walk(start_path):
        for file_name in files_name:
            if is_file_desired(file_name, pattern):
                path_to_module = create_path_to_module(current_dir_path, file_name)
                import_module(path_to_module, modules)
    return modules


def get_dirs_names_and_absolute_paths(start_absolute_path):
    import os
    dirs_names_and_paths = []
    for file_or_dir_name in os.listdir(start_absolute_path):
        absolute_file_or_dir_path = os.path.join(start_absolute_path, file_or_dir_name)
        if os.path.isdir(absolute_file_or_dir_path):
            dirs_names_and_paths.append((file_or_dir_name, absolute_file_or_dir_path))
    return dirs_names_and_paths
