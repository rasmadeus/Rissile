# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$18.10.2014 22:38:11$"

class Plugins:
    """    
    """
    def __init__(self):
        from rio.settings import settings
        self._settings = settings.Settings(
            (
                (
                    '/plugins/dir_search/',
                    self.get_dir_search,
                    self.set_dir_search,
                    'string'
                ),
            )
        )
        self._settings.read()     
    
    def find_availaible(self):
        from auxiliary import imp
        self._plugins_groups = {}
        for plugins_group_name, plugins_group_path in imp.get_dirs_names_and_absolute_paths(str(self._dir_search)):
            pass
   
    def set_dir_search(self, dir_search):
        self.remove_dir_search_from_sys_path()
        self._dir_search = dir_search
        self.append_dir_search_to_sys_path()
   
    def set_dir_search_with_user(self, dialog_parent):
        from PyQt4.QtGui import QFileDialog
        from PyQt4 import QtCore
        dialog_title = QtCore.QCoreApplication.translate('rio', QtCore.QString('Choose an initial dir'))
        dir = QFileDialog.getExistingDirectory(dialog_parent, dialog_title, self._dir_search)  
        if not dir.isEmpty():
            self.set_dir_search(dir)
            self._settings.save()        
        
    def append_dir_search_to_sys_path(self):
        import sys
        sys.path.append(str(self._dir_search))
        
    def remove_dir_search_from_sys_path(self):
        import sys
        try:
            sys.path.remove(self._dir_search)
        except:
            pass
        
    def get_dir_search(self):
        return self._dir_search