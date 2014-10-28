# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$23.06.2014 9:14:49$"


from PyQt4 import QtGui
class View(QtGui.QMainWindow):
    """
    Класс описывает главный интерфейс взаимодействия пользователя с доступными моделями.
    """
    def __init__(self, parent=None):
        """
        """       
        QtGui.QMainWindow.__init__(self, parent)
        self._load_ui()
        self._create_params_view()
        self._bind_actions()
        self._create_plugins()
        self._create_look_and_feel_settings()       

    def closeEvent(self, event):
        self._settings.save()
        return QtGui.QMainWindow.closeEvent(self, event)    
    
    def _load_ui(self):
        from PyQt4 import uic
        path_to_ui = 'view.ui'
        self._ui = uic.loadUiType(path_to_ui)[0]()
        self._ui.setupUi(self)
        
    def _create_params_view(self):
        from rio.params import view as params_view
        self._params_view = params_view.View(self)
        self._ui.values_setter.setWidget(self._params_view)
        self._params_view.model().restore_from_params({'car': 10, 'mass': 20})
    
    def _bind_actions(self):
        self._ui.exit.triggered.connect(self.close)
    
    def _create_plugins(self):       
        from rio.plugins.plugins import Plugins
        self._plugins = Plugins()
        self._plugins._logger = self._ui.logger
        self._ui.action_set_dir_search.triggered.connect(self._set_plugins_dir_search_with_user)
        self._update_plugins_menu()
    
    def _set_plugins_dir_search_with_user(self):
        self._plugins.set_dir_search_with_user(self)
        self._update_plugins_menu()
    
    def _update_plugins_menu(self):
        self._plugins.find()
        self._plugins.fill_menu(self._ui.menu_open_plugin)
        
    def _create_look_and_feel_settings(self):
        from rio.settings import settings
        self._settings = settings.Settings(
            (
                ( 
                    'view/geometry', 
                    self.saveGeometry,
                    self.restoreGeometry,
                   'byte_array'
                ),
                (
                    'view/state', 
                    self.saveState,  
                    self.restoreState, 
                    'byte_array'
                ),
                (
                    'view/setting_setter_visibility', 
                    self._ui.values_setter.isVisible, 
                    self._ui.show_values_setter.setChecked,
                    'bool'
                ),
                (
                    'view/online_logger_visibility', 
                    self._ui.online_logger.isVisible, 
                    self._ui.show_online_logger.setChecked, 
                    'bool'
                )        
            )
        )
        self._settings.read()