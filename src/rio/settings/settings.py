# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$18.10.2014 22:41:51$"

SETTINGS_FILE_NAME = 'rio_settings.ini'

class Settings:
    """    
    """
    def __init__(self, properties):
        from PyQt4 import QtCore
        self._settings = QtCore.QSettings('rio_settings.ini', QtCore.QSettings.IniFormat)
        self._properties = properties
        
    def save(self):
        for property in self._properties:
            self._settings.setValue(property[0], property[1]())
            
    def read(self):
        def value(value, type):
            if type == 'byte_array': return value.toByteArray()
            if type == 'bool': return value.toBool()
            if type == 'string': return value.toString()
            return value.toDouble()
        
        for property in self._properties:
            property[2](value(self._settings.value(property[0]), property[3]))
    
   
