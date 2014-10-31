# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$29.10.2014 18:34:31$"

from PyQt4 import QtGui
from PyQt4 import QtCore
import os
from tools import settings

class Translator:
    def __init__(self):
        self._active_rio_locale = ''
        self._translations_dir = os.path.join(os.getcwd(), 'tr')
        self._translator_agents = []
        self._rio_tr = QtCore.QTranslator()
        self._base_qt_tr = QtCore.QTranslator()
        self._install_translations()
        self._settings = settings.Settings(
            (
                ( 
                    'tr/locale', 
                    self.get_active_rio_locale,
                    self.set_active_rio_locale,
                    'string'
                ),
            )
        )
        
    def restore_active_rio_locale(self):
        self._settings.read()
        
    def save_active_rio_locale(self):
        self._settings.save()
        
    def get_active_rio_locale(self):
        return self._active_rio_locale
    
    def set_active_rio_locale(self, rio_locale):
        self._active_rio_locale = str(rio_locale)
        
    def set_translations_dir(self, there_are_translations):
        self._translations_dir = there_are_translations
        
    def fill_with_availaible_translations(self, menu):
        actions = QtGui.QActionGroup(menu)
        self._add_native_locale(actions)
        self._add_availaible_locales(actions)
        menu.addActions(actions.actions())
        actions.triggered.connect(self._change_locale)
    
    def load_locale(self, locales_names):
        self._active_rio_locale = locales_names[0]
        self._rio_tr.load(locales_names[0], self._translations_dir)
        self._base_qt_tr.load(locales_names[1], self._translations_dir)
        self._call_translator_agents()
    
    def add_translator_agent(self, agent_callable):
        self._translator_agents.append(agent_callable)
        
    def _call_translator_agents(self):
        for translator_agent in self._translator_agents:
            translator_agent()
            
    def _add_to_qt_ts_file_language_name(self):
        QtCore.QCoreApplication.translate('rio', 'English')
        
    def _install_translations(self):
        QtGui.QApplication.installTranslator(self._base_qt_tr)
        QtGui.QApplication.installTranslator(self._rio_tr)
        
    def _change_locale(self, action):
        locales_names = action.data().toPyObject()
        self.load_locale(locales_names)
      
    def _create_locale_action(self, name, locales, parent):
        action = QtGui.QAction(name, parent)
        action.setCheckable(True)
        action.setData(locales)
        self._check_for_active_locale(action)
        return action
        
    def _check_for_active_locale(self, action):
        if action.data().toPyObject()[0] == self._active_rio_locale:
            action.setChecked(True)
            self._change_locale(action)
        
    def _add_native_locale(self, actions):
        name = self._get_native_locale()
        locales = ('', '')
        action = self._create_locale_action(name, locales, actions)
        actions.addAction(action)
        
    def _get_native_locale(self):
        return 'English'
        
    def _get_locale_name(self, rio_locale):
        translator = QtCore.QTranslator()
        translator.load(rio_locale, self._translations_dir)
        return translator.translate('rio', self._get_native_locale())
        
    def _add_availaible_locales(self, actions):
        import fnmatch
        for rio_locale in os.listdir(self._translations_dir):
            if fnmatch.fnmatch(rio_locale, 'rio_*.qm'):                
                name = self._get_locale_name(rio_locale)
                locales = self._get_locales_names(rio_locale)
                action = self._create_locale_action(name, locales, actions)
                actions.addAction(action)
        
    def _add_english_locale(self):
        self._add_locale('en', self._get_native_locale())
        
    def _get_locale_suffix(self, rio_locale):
        try:
            return rio_locale.split('.')[0].split('_')[1]
        except:
            return ''    
    
    def _get_qtbase_locale(self, suffix):
        return 'qt_base_' + suffix + '.qm'
    
    def _get_locales_names(self, rio_locale):
        suffix = self._get_locale_suffix(rio_locale)
        qtbase_locale = self._get_qtbase_locale(suffix)
        return (rio_locale, qtbase_locale)
    
    
    