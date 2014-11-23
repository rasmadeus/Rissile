# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$Nov 19, 2014 10:40:11 AM$"

class ModuleChecker():
    class ModuleImportError(Exception):
        def __init__(self, comment):
            Exception.__init__(self)
            self.comment = comment 
    
    def __init__(self, logger, attrs):
        self._logger = logger
        self._attrs = attrs
        
    @staticmethod
    def _check_for_having_attr(module, attr_name):
        if not hasattr(module, attr_name):
            base = QtCore.QCoreApplication.translate(
                'rio',
                ' has not attribute '
            )
            raise ModuleImportError(module + base + attr_name)
       
    @staticmethod
    def _check_for_instance(plugin, attr_name, attr_type):
        if not isinstance(getattr(plugin, attr_name), attr_type):
            base = QtCore.QCoreApplication.translate(
                'rio',
                ' is not '
            )
            raise ModuleImportError(attr_name + base + str(attr_type))
        
    def _find_errors(self, module):
        for attr_name, attr_type in self._attrs:
            ModuleChecker._check_for_having_attr(module, attr_name)
            ModuleChecker._check_for_instance(module, attr_name, attr_type)
        
    def is_valid(self, module):
        try:
            self._find_errors(module)
            return True
        except ModuleChecker.ModuleImportError as error:
            self._logger.write_error(error.comment)
            return False


class ModuleImporter:
    """
    
    """
    def __init__(self, logger, attrs):
        self._logger = logger
        self._attrs = attrs
        self.unload_module()

    def unload_module(self):
        self._module = None  

    def get_module(self):
        return self._module

    def is_imported(self):
        return False if self._module is None else True

    def load(self, path_to_module):
        self.unload_module()
        self._try_import_valid_module(path_to_module)
            
    def _try_import_valid_module(self, path_to_module):
        import importlib
        try:
            imported_module = importlib.import_module(path_to_module)
            self._set_module_if_valid(imported_module)              
        except ImportError:
             self._write_import_error(path_to_module)
            
    def _set_module_if_valid(self, imported_module):
        module_checker = ModuleChecker(self._logger, self._attrs)
        if module_checker.is_valid(imported_module):
            self._module = imported_module 
            
    def _write_import_error(self, path_to_module):
        base = QtCore.QCoreApplication.translate(
            'rio', 
            ' is not able for importing!'
        )            
        self._logger.write_error(path_to_module + base)

