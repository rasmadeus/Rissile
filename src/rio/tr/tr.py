# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$29.10.2014 18:34:31$"

from PyQt4 import QtGui
from PyQt4 import QtCore
import os

class Translator:
    def __init__(self, menu_languages):
        self._PATH_TO_TR = os.path.join(os.getcwd(), 'tr')
        self._actions = QtGui.QActionGroup(menu_languages)
        self._fill_menu_languages(menu_languages)
        self._rio_tr = QtCore.QTranslator()
        self._base_qt_tr = QtCore.QTranslator()
        self._install_trs()
        
    def _install_trs(self):
        QtGui.QApplication.installTranslator(self._base_qt_tr)
        QtGui.QApplication.installTranslator(self._rio_tr)
        
    def _add_english_locale(self):
        self._add_locale('en', 'English')
    
    def _add_availaible_locales(self):
        pass
    
    def _fill_menu_languages(self, menu_languages):
        self._add_english_locale()
        self._add_availaible_locales()
        menu_languages.addActions(self._actions.actions())
        
    def _add_locale(self, locale_suffix, locale_name):
        action = QtGui.QAction(locale_name, self._actions)
        action.setCheckable(True)
        action.setData(locale_suffix)
        self._actions.addAction(action)
