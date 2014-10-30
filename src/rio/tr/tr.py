# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$29.10.2014 18:34:31$"

from PyQt4 import QtGui
from PyQt4 import QtCore
import os

class Translator:
    def __init__(self, menu_languages, retranslator):
        QtCore.QCoreApplication.translate('rio', 'English')
        self._PATH_TO_TR = os.path.join(os.getcwd(), 'tr')
        self._retranslator = retranslator
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
        import fnmatch
        for file_or_dir in os.listdir(self._PATH_TO_TR):
            if fnmatch.fnmatch(file_or_dir, 'rio_*.qm'):
                translator = QtCore.QTranslator()
                translator.load(file_or_dir, self._PATH_TO_TR)
                language = translator.translate('rio', 'English')
                self._add_locale(file_or_dir, language)
    
    def _fill_menu_languages(self, menu_languages):
        self._add_english_locale()
        self._add_availaible_locales()
        menu_languages.addActions(self._actions.actions())
        self._actions.triggered.connect(self._change_locale)
        
    def _add_locale(self, locale_suffix, language):
        action = QtGui.QAction(language, self._actions)
        action.setCheckable(True)
        action.setData(locale_suffix)
        self._actions.addAction(action)        
        
    def _get_suffix_from(self, language):
        try:
            return language.split('.')[0].split('_')[1]
        except:
            return 'en'       
        
    def _get_qtbase_locale_name(self, suffix):
        return 'qtbase_' + suffix + '.'
        
    def _change_locale(self, action):
        language = action.data().toPyObject()        
        language_suffix = self._get_suffix_from(language)
        qtbase_locale_name = self._get_qtbase_locale_name(language_suffix)
        self._rio_tr.load(language, self._PATH_TO_TR)
        self._base_qt_tr.load(qtbase_locale_name, self._PATH_TO_TR)
        self._retranslator()