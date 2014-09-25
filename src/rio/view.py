# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$23.06.2014 9:14:49$"


from PyQt4 import QtCore, QtGui, uic
from rio.params import view as params_view
from model_executor import RissileModelExecutor

class View(QtGui.QMainWindow):
    """
    Класс описывает главный интерфейс взаимодействия пользователя с доступными моделями.
    """
    def __init__(self, rissile_models, parent=None):
        """
        :param rissile_models: набор доступных моделей.
        :type rissile_models: {'ключ группы модели': ('имя группы модели': (('имя модели', функция производящая модель), ...), ...), ...}
        """
        def create_settings_paths():
            self._geometry_path = '/view/geometry'
            self._state_path = '/view/state'     
            self._values_setter_path = 'view/setting_setter_visibility'
            self._online_logger_path = 'view/online_logger_visibility'

        def append_properties():
            form, base = uic.loadUiType("view.ui")
            self.ui = form()
            self.ui.setupUi(self)

        def restore_state():
            settings = self._settings()
            self.restoreGeometry(settings.value(self._geometry_path).toByteArray())
            self.restoreState(settings.value(self._state_path).toByteArray())
            self.ui.action_show_values_setter.setChecked(settings.value(self._values_setter_path).toBool())
            self.ui.action_show_online_logger.setChecked(settings.value(self._online_logger_path).toBool())

        def create_view():
            view = params_view.View(self)
            self.ui.values_setter.setWidget(view)
            self._values_setter_view = view
 
        def create_rissile_models_menu():
            rissile_models.fill_menu(self.ui.menu_models, self._create_new_project)
            
        def create_executor():
            self._rissile_model_executor = RissileModelExecutor(self.ui.text_shower)
            
        def create_connections():
            self.ui.action_exit.triggered.connect(self.close)
            
            
        QtGui.QMainWindow.__init__(self, parent)
        create_settings_paths()
        append_properties()
        create_view()
        create_connections()
        create_rissile_models_menu()
        create_executor()
        restore_state()


    def _create_new_project(self, action):
        self._model = action.data().toPyObject()()
        self._values_setter_view.model().restore_from_params(self._model.origin_state())
        self.setWindowTitle(QtCore.QObject().tr('Model is') + action.text())
        self._rissile_model_executor.set_model_creator(self._model)
        self._rissile_model_executor.set_generator(self._values_setter_view.model().generator())
    

    def closeEvent(self, event):
        def save_state():
            settings = self._settings()
            settings.setValue(self._geometry_path, self.saveGeometry())
            settings.setValue(self._state_path, self.saveState())
            settings.setValue(self._values_setter_path, self.ui.values_setter.isVisible())
            settings.setValue(self._online_logger_path, self.ui.online_logger.isVisible())
        save_state()
        return QtGui.QMainWindow.closeEvent(self, event)


    def _settings(self):
        """
        :return: инициализированный экземпляр QSettings для записи настроек self.
        """
        return QtCore.QSettings('rio_settings.ini', QtCore.QSettings.IniFormat)  