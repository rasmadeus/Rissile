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
        for plugins_group_name, plugins_group_path in imp.get_dirs_names_and_absolute_paths(self._dir_search):
            availaible_dirs_and_paths = imp.get_dirs_names_and_absolute_paths(plugins_group_path)
            plugins_group_module = plugins_group_name + '.info'
            self._plugins_groups[plugins_group_module] = []
            for plugin_name, plugin_path in availaible_dirs_and_paths:
                plugin_module_path = plugins_group_name + '.' + plugin_name + '.plugin'
                self._plugins_groups[plugins_group_module].append(plugin_module_path)
                
    def set_dir_search(self, dir_search):
        self.remove_dir_search_from_sys_path()
        self._dir_search = str(dir_search)
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
        sys.path.append(self._dir_search)
        
    def remove_dir_search_from_sys_path(self):
        import sys
        try:
            sys.path.remove(self._dir_search)
        except:
            pass
        
    def get_dir_search(self):
        return self._dir_search
    
    def fill_menu(self, menu):
        from auxiliary import imp
        
        def fill_sub_menu_by(sub_menu, plugins_maybe):
            for plugin_module_name in plugins_maybe:
                imported_plugin_module = imp.get_imported_module(plugin_module_name)
                if imported_plugin_module is not None:
                    try:
                        plugin_name = imported_plugin_module.PLUGIN_NAME
                        action = sub_menu.addAction(plugin_name)
                        action.setData(plugin_name)
                    except:
                        pass
        
        def create_sub_menu(plugins_group_module, plugins_maybe, menu):
            imported_plugins_group_module = imp.get_imported_module(plugins_group_module)
            if imported_plugins_group_module is not None:
                try:
                    plugins_group_name = imported_plugins_group_module.PLUGINS_GROUP_NAME
                    fill_sub_menu_by(menu.addMenu(plugins_group_name), plugins_maybe)
                except:
                    pass

        menu.clear()
        for plugins_group_module, plugins_maybe in self._plugins_groups.iteritems():
           create_sub_menu(plugins_group_module, plugins_maybe, menu)
            