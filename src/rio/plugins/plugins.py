# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$18.10.2014 22:38:11$"

class Plugin:
    def get_default_state(self):
        pass
    
    def set_initial_state(self, params):
        pass
    
    def run(self):
        pass
    
    def call(self, out_agent):
        pass   



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
    
    def find(self):    
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
        import importlib
        
        def fill_sub_menu_by(sub_menu, plugins_maybe):
            for plugin_module_name in plugins_maybe:
                try:
                    imported_plugin_module = importlib.import_module(plugin_module_name)
                    plugin_name = imported_plugin_module.NAME
                    action = sub_menu.addAction(plugin_name)
                    plugin_short_description = imported_plugin_module.SHORT_DESCRIPTION
                    action.setStatusTip(plugin_short_description)
                    action.setData(plugin_name)
                except:
                    pass
        
        def create_sub_menu(plugins_group_module, plugins_maybe, menu): 
            from PyQt4 import QtCore
            try:
                imported_plugins_group_module = importlib.import_module(plugins_group_module)
                plugins_group_name = imported_plugins_group_module.NAME
                sub_menu = menu.addMenu(plugins_group_name)
                fill_sub_menu_by(sub_menu, plugins_maybe)
            except ImportError:
                comment = QtCore.QCoreApplication.translate(
                    'rio', 
                    QtCore.QString('It\'s impossible to import %1').arg(plugins_group_module)
                )                
                self._logger.append(comment)
            except AttributeError:
                comment = QtCore.QCoreApplication.translate(
                    'rio', 
                    QtCore.QString('%1 must have the NAME attribute!').arg(plugins_group_module)
                )                
                self._logger.append(comment)

        menu.clear()
        for plugins_group_module, plugins_maybe in self._plugins_groups.iteritems():
            create_sub_menu(plugins_group_module, plugins_maybe, menu)
            