# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from PyQt4 import QtGui

class Log(QtGui.QTextEdit):
    """    
    """
    def __init__(self, parent):
        QtGui.QTextEdit.__init__(self, parent)
        self.setReadOnly(True)
        
    def _write(self, color, text):
        from time import gmtime, strftime
        self.setTextColor(color)
        self.append(strftime("%H:%M:%S\t", gmtime()) + text)
        
    def write_info(self, info):
        self._write(QtGui.QColor(0, 0, 0), info)
        
    def write_warning(self, warning):
        self._write(QtGui.QColor(255, 255, 0), warning)
        
    def write_error(self, error):
        self._write(QtGui.QColor(255, 0, 0), error)
        
