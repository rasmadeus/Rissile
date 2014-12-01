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
        self._create_log()
        self._create_params_view()
        self._bind_actions()
        self._create_look_and_feel_settings()   
        self._create_translator()
        self._create_plugins_executor()
        self._create_plugins_manager()


    def closeEvent(self, event):
        self._settings.save()
        return QtGui.QMainWindow.closeEvent(self, event)    
    
    def _load_ui(self):
        from PyQt4 import uic
        path_to_ui = 'view.ui'
        self._ui = uic.loadUiType(path_to_ui)[0]()
        self._ui.setupUi(self)
        
    def _create_log(self):
        from log import Log
        self._log = Log(self._ui.online_log)
        self._ui.online_log.setWidget(self._log)
        
        
    def _create_params_view(self):
        from rissile.rio.params import view as params_view
        self._params_view = params_view.View(self)
        self._ui.values_setter.setWidget(self._params_view)
    
    def _bind_actions(self):
        self._ui.exit.triggered.connect(self.close)
    
    def _create_look_and_feel_settings(self):
        from tools import settings
        self._settings = settings.Settings(self._get_settings())
        self._settings.read()
        
    def _get_settings(self):
        return \
        (
            self._get_geometry_settings(),
            self._get_state_settings(),
            self._get_params_view_state_settings(),
            self._get_log_state_settings()
        )
        
    def _get_geometry_settings(self):
        return \
        ( 
            'view/geometry', 
            self.saveGeometry,
            self.restoreGeometry,
            'byte_array'
        )
        
    def _get_state_settings(self):
        return \
        (
            'view/state', 
            self.saveState,  
            self.restoreState, 
            'byte_array'
        )
        
    def _get_params_view_state_settings(self):
        return \
        (
            'view/setting_setter_visibility', 
            self._ui.values_setter.isVisible, 
            self._ui.show_values_setter.setChecked,
            'bool'
        )
        
    def _get_log_state_settings(self):
        return \
        (
            'view/online_log_visibility', 
            self._ui.online_log.isVisible, 
            self._ui.show_online_log.setChecked, 
            'bool'
        )        
        
    def _create_translator(self):
        from tr import tr
        self._tr = tr.Translator()
        self._tr.add_translator_agent(self._retranslate)
        self._tr.fill_with_availaible_translations(self._ui.menu_languages)
        
    def _retranslate(self):
        self._ui.retranslateUi(self)

    def _create_plugins_manager(self):
        from plugins import plugins
        self._plugins_manager = plugins.PluginsManager(self._log, self)
        self._plugins_manager.location_was_changed.connect(self._fill_plugins_menu)
        self._plugins_manager.plugin_was_choosen.connect(self._notify_parts_about_new_plugin)
        self._plugins_manager.fill(self._ui.menu_open_plugin) 
        self._ui.action_set_dir_search.triggered.connect(self._set_plugins_location_by_user)
        
    def _set_plugins_location_by_user(self):
        self._plugins_manager.set_location_by_user(self)
        
    def _fill_plugins_menu(self):
        self._plugins_manager.fill(self._ui.menu_open_plugin)
        
    def _notify_parts_about_new_plugin(self, action):
        plugin_module = action.data().toPyObject()
        self._params_view.restore_from_plugin(plugin_module)
        self._executor.set_plugin(plugin_module)
        
    def _lock_interface(self):
        self._ui.run.setEnabled(False)
        self._ui.stop.setEnabled(True)
        self._ui.menu_plugins.setEnabled(False)
    
    def _unlock_interface(self):
        self._ui.run.setEnabled(True)
        self._ui.stop.setEnabled(False)
        self._ui.menu_plugins.setEnabled(True)
        
    def _create_plugins_executor(self):
        from rissile.rio.plugins import executor
        self._executor = executor.Executor(self._log, self._params_view.generator, self)
        self._executor.start_running.connect(self._lock_interface)
        self._executor.stop_running.connect(self._unlock_interface)
        self._ui.run.triggered.connect(self._executor.run)
        self._ui.stop.triggered.connect(self._executor.stop)