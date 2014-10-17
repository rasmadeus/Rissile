# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$23.06.2014 9:14:49$"


from PyQt4 import QtCore, QtGui, uic
from rio.params import view as params_view

class View(QtGui.QMainWindow):
    """
    Класс описывает главный интерфейс взаимодействия пользователя с доступными моделями.
    """
    def __init__(self, parent=None):
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
            self._values_setter_view.model().restore_from_params({'car': 10, 'mass': 20})
 
        def create_connections():
            self.ui.action_exit.triggered.connect(self.close)
            
            
        QtGui.QMainWindow.__init__(self, parent)
        create_settings_paths()
        append_properties()
        create_view()
        create_connections()
        restore_state()


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