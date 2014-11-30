# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="rasmadeus"
__date__ ="$16.10.2014 21:43:57$"

def create_path_to_module(current_dir_path, file_name):
    path_to_module = '.'.join([current_dir_path, file_name.split('.')[0]])
    return  path_to_module[2:].replace('\\','.')

def import_module(path_to_module):
     import importlib
     try:
        module = importlib.import_module(path_to_module)
        return module
     except:
        return  None

def get_all_imported_modules(start_path, pattern='\S+\.py'):
    def is_file_desired(file_name, pattern):
        import re
        try:
            return re.compile(pattern).match(file_name) != None
        except:
            return False
    
    import os
    
    for current_dir_path, dirs_name, files_name in os.walk(start_path):
        for file_name in files_name:
            if is_file_desired(file_name, pattern):
                path_to_module = create_path_to_module(current_dir_path, file_name)
                module = import_module(path_to_module)
                if module is not None:
                    yield module
                    
                    
def get_dirs(start_path):
    import os
    try:
        for file_or_dir in os.listdir(start_path):
            if os.path.isdir(os.path.join(start_path, file_or_dir)):
                yield file_or_dir
    except WindowsError:
        pass                
