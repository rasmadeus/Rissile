# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$Nov 23, 2014 4:38:32 PM$"

class Plugin:
    """
    """
    def get_default_state(self):
        pass
    
    def set_initial(self, state):
        pass
    
    def run(self):
        pass    
    

class _ModuleContentError(Exception):
    """
    """
    def __init__(self,error_comment):
        self._error_comment = error_comment
        
    def write_comment_error(self, log):
        log.write_error(self._error_comment)

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
        import importlib
        try:
            module = importlib.import_module(path)
            self._valid(module, attrs)
            self._module = module
        except ImportError:
            self._log()
        except _ModuleContentError as content_error:
            content_error.write_comment_error(self._log)
            
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
            
    def _log(self):
        base_message = QtCore.QCoreApplication.translate('rio', ' isn\'t able for importing.')
        self._log.write_error(path + base_message)

class _Location:
    """
    """
    def __init__(self, location = ''):
        self._location = location
        
    def get_dirs(self):
        from tools import imp
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
    
    def _get_path(self, dir):
        pass
    
    def _process_valid(self, module, dir):
        pass
    
    def _clear(self):
        self._container = []
    
    def find(self):
        self._clear()        
        for dir in self._location.get_dirs():
            module = _Module(self._log)
            module.load(self._get_path(dir), self._get_attrs())
            if module.is_valid():
                self._process_valid(module.get_module(), dir)

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
    
    def _get_path(self, dir):
        return self._path + '.' + dir + '.plugin'
     
    def _process_valid(self, module, dir):
        self._container.append(module)
        
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
    
    def _get_path(self, dir):
        return dir + '.info'
    
    def _process_valid(self, module, dir):
        group = _Group(
            self._log,
            self._location.get_sub_location(dir),
            dir,
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
        from tools import settings
        QtCore.QObject.__init__(self, parent)
        self._log = log
        self._groups = Groups(log)        
        self._settings = settings.Settings(
            (
                (
                    '/plugins/location/',
                    self.get_location,
                    self.set_location,
                    'string'
                ),
            )
        )
        self._settings.read()  
        
    def set_location(self, location):
        self._say_that_plugins_searching_is_started()
        self._groups.set_location(str(location))
        self._groups.find()
        self.location_was_changed.emit()
        self._settings.save()
        self._say_that_plugins_searching_is_ended()
        
    def _say_that_plugins_searching_is_started(self):
        info = QtCore.QCoreApplication.translate('rio', 'Plugins\' searching is started.')
        self._log.write_info(info)
    
    def _say_that_plugins_searching_is_ended(self):
        info = QtCore.QCoreApplication.translate('rio', 'Plugins\' searching was ended.')
        self._log.write_info(info)
        
    def get_location(self):
        return self._groups.get_location()
    
    def set_location_by_user(self, dialog_parent):
        from PyQt4.QtGui import QFileDialog
        dialog_title = QtCore.QCoreApplication.translate('rio', 'Choose an initial dir')
        dir = QFileDialog.getExistingDirectory(dialog_parent, dialog_title, self.get_location())  
        if not dir.isEmpty():
            self.set_location(dir)
            
    def fill(self, menu):
        menu.clear()
        self._groups.fill(menu, self.plugin_was_choosen)
    

