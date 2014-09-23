# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$10.07.2014 10:39:07$"


from PyQt4 import QtCore, QtGui


class Delegate(QtGui.QItemDelegate):
    """
    """
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        self._delegate = index.internalPointer().delegate(parent)
        return self._delegate.createEditor(parent, option, index)


    def setEditorData(self, editor, index):
        self._delegate.setEditorData(editor, index)


    def setModelData(self, editor, model, index):
        self._delegate.setModelData(editor, model, index)