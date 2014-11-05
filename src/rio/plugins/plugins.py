# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$18.10.2014 22:38:11$"

class Plugin:
    def get_default_state(self):
        return {}
    
    def set_initial_state(self, params):
        pass
    
    def run(self):
        pass
    
    def call(self, out_agent):
        pass   


class _PluginsFinder():
    
    def __init__(self, logger):
        self._logger = logger
        self._attrs = (('NAME', str),)
    
    @staticmethod
    def get_path_to_plugin(plugins_group_name, plugin_name): 
        return plugins_group_name + '.' + plugin_name + '.plugin'
   
    @staticmethod
    def get_path_to_group(plugins_group_name):
        return plugins_group_name + '.info'
    
    def find(self, dir_search):
        from tools import imp
        self._clear_prev_founded_plugins_group()
        dirs_and_names = imp.get_dirs_names_and_absolute_paths(dir_search)
        for plugins_group_name, plugins_group_path in dirs_and_names: 
            self._add_group(plugins_group_name, plugins_group_path)
        
    def get_plugins_groups(self):
        return self._plugins_groups
        
    def _clear_prev_founded_plugins_group(self):
        self._plugins_groups = {}
            
    def _add_group(self, plugins_group_name, plugins_group_path):
        path_to_group = self.get_path_to_group(plugins_group_name)
        self._call_if_importable(path_to_group, self._add_valid_group, plugins_group_name, plugins_group_path)
            
    def _add_valid_group(self, group, plugins_group_name, plugins_group_path):
        from tools import imp
        self._plugins_groups[group.NAME] = []
        availaible_dirs_and_paths = imp.get_dirs_names_and_absolute_paths(plugins_group_path)
        for plugin_name, plugin_path in availaible_dirs_and_paths:
            self._add_plugin(plugins_group_name, plugin_name, group)
            
    def _add_plugin(self, plugins_group_name, plugin_name, group):
        path_to_plugin = self.get_path_to_plugin(plugins_group_name, plugin_name)
        self._call_if_importable(path_to_plugin, self._plugins_groups[group.NAME].append)
          
    def _call_if_importable(self, path_to_module, f, *f_args):
        from loader import ModuleImporter
        importer = ModuleImporter(self._logger, self._attrs)
        importer.load(path_to_module)
        if(importer.is_imported()):
            f(importer.get_module(), *f_args)
            
    
from PyQt4 import QtCore
from PyQt4 import QtGui
class Plugins(QtCore.QObject):
    """    
    """
    change_plugin = QtCore.pyqtSignal(QtGui.QAction)
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        from tools import settings
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
        plugins_finder = _PluginsFinder(self._logger)
        plugins_finder.find(self._dir_search)  
        self._plugins_groups = plugins_finder.get_plugins_groups()
                
    def set_dir_search(self, dir_search):
        self.remove_dir_search_from_sys_path()
        self._dir_search = str(dir_search)
        self.append_dir_search_to_sys_path()
   
    def set_dir_search_with_user(self, dialog_parent):
        from PyQt4.QtGui import QFileDialog
        dialog_title = QtCore.QCoreApplication.translate('rio', 'Choose an initial dir')
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
        menu.clear()
        for plugins_group_name, plugins in self._plugins_groups.iteritems():
            sub_menu = menu.addMenu(plugins_group_name)
            actions = QtGui.QActionGroup(sub_menu)
            self._fill_sub_menu_by(actions, plugins)
            sub_menu.addActions(actions.actions())
            
    def _fill_sub_menu_by(self, actions, plugins):
        for plugin in plugins:
            action = QtGui.QAction(plugin.NAME, actions)
            action.setStatusTip(plugin.SHORT_DESCRIPTION)
            action.setData(plugin)
            actions.addAction(action)
            actions.triggered.connect(self.change_plugin)