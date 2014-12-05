# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$Nov 23, 2014 4:38:32 PM$"

class Plugin:
    """
    """
        
    def get_default_state(self):
        return {}
    
    def set_initial(self, state):
        pass
    
    def run(self):
        while self.must_live_until():
            self._run()
    
    def save_states(self):
        pass
    
    def must_live_until(self):
        return True    
    
    
    def __call__(self, initial_state):
        self.set_initial(initial_state['Model\'s params'])
        self.run()
        
    def _run(self):
        pass
    

class _ModuleContentError(Exception):
    """
    """
    def __init__(self,error_comment):
        self._error_comment = error_comment
        
    def write_comment_error(self, log):
        log.error(self._error_comment)

from PyQt4 import QtCore
class _Module:
    """
    """
    def __init__(self, log):
        self._module = None
        self._log = log
        
    def get_module(self):
        return self._module
    
    def is_valid(self):
        return False if self._module is None else True
    
    def load(self, path, attrs = ()):        
        try:
            self._load(path, attrs)
        except ImportError:
            self._say_about_import_error(path)
        except _ModuleContentError as content_error:
            content_error.write_comment_error(self._log)
            
    def _load(self, path, attrs):
        import importlib
        module = importlib.import_module(path)
        self._valid(module, attrs)
        self._module = module
            
    def _valid(self, module, attrs):
        for attr_name, attr_type in attrs:
            self._raise_if_hasnot(module, attr_name)
            self._raise_if_isnot(module, attr_name, attr_type)
            
    def _raise_if_hasnot(self, module, attr_name):
        if not hasattr(module, attr_name):
            base_message = QtCore.QCoreApplication.translate('rio', ' hasn\'t attr ')
            raise _ModuleContentError(str(module) + base_message + attr_name)
    
    def _raise_if_isnot(self, module, attr_name, attr_type):
        attr = getattr(module, attr_name)
        if not isinstance(attr, attr_type):
            if not isinstance(attr(), attr_type):
                base_message = QtCore.QCoreApplication.translate('rio', ' isn\'t ')
                raise _ModuleContentError(str(module) + '.' + attr_name + base_message + str(attr_type))
            
    def _say_about_import_error(self, path):
        base_message = QtCore.QCoreApplication.translate('rio', ' isn\'t able for importing.')
        self._log.error(path + base_message)

class _Location:
    """
    """
    def __init__(self, location = ''):
        self._location = location
        
    def get_dirs(self):
        from rissile.rio.tools import imp
        return imp.get_dirs(self._location)
    
    def get_location(self):
        return self._location
    
    def set_location(self, location):
        self._location = location
        
    def get_sub_location(self, subdir):
        import os
        return _Location(os.path.join(self._location, subdir))
    
class _GroupsLocation(_Location):
    """
    """   
    def set_location(self, location):
        self._remove_from_sys_path()
        self._location = location
        self._append_to_sys_path()
        
    def _append_to_sys_path(self):
        import sys
        sys.path.append(self._location)
        
    def _remove_from_sys_path(self):
        import sys
        try:
            sys.path.remove(self._location)
        except:
            pass

class _ModuleContainer:
    """
    """
    def __init__(self, log, location):
        self._log = log
        self._location = location
        self._container = []
        
    def _get_attrs(self):
        pass
    
    def _get_path(self, dir_name):
        pass
    
    def _process_valid(self, module, dir_name):
        pass
    
    def _clear(self):
        self._container = []
    
    def find(self):
        self._clear()        
        for dir_name in self._location.get_dirs():
            module = _Module(self._log)
            module.load(self._get_path(dir_name), self._get_attrs())
            if module.is_valid():
                self._process_valid(module.get_module(), dir_name)

from PyQt4 import QtGui
class _Group(_ModuleContainer):
    """
    """
    def __init__(self, log, location, path, info_module):
        _ModuleContainer.__init__(self, log, location)
        self._path = path
        self._info_module = info_module
     
    def _get_attrs(self):
        return (('NAME', str), ('SHORT_DESCRIPTION', str), ('Plugin', Plugin))
    
    def _get_path(self, dir_name):
        return self._path + '.' + dir_name + '.plugin'
     
    def _process_valid(self, module, dir_name):  
        self._say_that_plugin_was_found(module)
        self._container.append(module)
        
    def _say_that_plugin_was_found(self, module):
        info = QtCore.QCoreApplication.translate('rio', ' was found.')
        self._log.info(str(module) + info)
        
    def fill(self, menu, f):
        sub_menu = menu.addMenu(self._info_module.NAME)
        actions = QtGui.QActionGroup(sub_menu)
        for plugin in self._container:
            action = QtGui.QAction(plugin.NAME, actions)
            action.setStatusTip(plugin.SHORT_DESCRIPTION)
            action.setData(plugin)
            actions.addAction(action)
            actions.triggered.connect(f)
        sub_menu.addActions(actions.actions())

class Groups(_ModuleContainer):
    """    
    """
    def __init__(self, log):
        _ModuleContainer.__init__(self, log, _GroupsLocation())
        
    def set_location(self, location):
        self._location.set_location(location)
        
    def get_location(self):
        return self._location.get_location()
    
    def _get_attrs(self):
        return (('NAME', str),)
    
    def _get_path(self, dir_name):
        return dir_name + '.info'
    
    def _process_valid(self, module, dir_name):
        group = _Group(
            self._log,
            self._location.get_sub_location(dir_name),
            dir_name,
            module
        )
        group.find()
        self._container.append(group)
        
    def fill(self, menu, f):
        for group in self._container:
            group.fill(menu, f)
        
class PluginsManager(QtCore.QObject):
    """    
    """
    location_was_changed = QtCore.pyqtSignal()
    plugin_was_choosen = QtCore.pyqtSignal(QtGui.QAction)
    
    def __init__(self, log, parent):
        QtCore.QObject.__init__(self, parent)
        self._log = log
        self._groups = Groups(log)      
        self._create_settings()
        
    def set_location(self, location):
        self._say_that_plugins_searching_is_started()
        self._groups.set_location(str(location))
        self._groups.find()
        self.location_was_changed.emit()
        self._settings.save()
        self._say_that_plugins_searching_is_ended()
        
    def get_location(self):
        return self._groups.get_location()
    
    def set_location_by_user(self, dialog_parent):
        from PyQt4.QtGui import QFileDialog
        dialog_title = QtCore.QCoreApplication.translate('rio', 'Choose an initial dir_name')
        dir_name = QFileDialog.getExistingDirectory(dialog_parent, dialog_title, self.get_location())  
        if not dir_name.isEmpty():
            self.set_location(dir_name)
            
    def fill(self, menu):
        menu.clear()
        self._groups.fill(menu, self.plugin_was_choosen)
        
    def _say_that_plugins_searching_is_started(self):
        info = QtCore.QCoreApplication.translate('rio', 'Plugins\' searching is started.')
        self._log.info(info)
    
    def _say_that_plugins_searching_is_ended(self):
        info = QtCore.QCoreApplication.translate('rio', 'Plugins\' searching was ended.')
        self._log.info(info)
        
    def _create_settings(self):
        from rissile.rio.tools import settings
        self._settings = settings.Settings((self._get_location_settings(),))
        self._settings.read() 
        
    def _get_location_settings(self):
        return \
        ( \
            '/plugins/location/', \
            self.get_location, \
            self.set_location,
            'string' \
        )