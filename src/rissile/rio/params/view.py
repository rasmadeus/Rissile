# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$11.07.2014 13:57:02$"


from PyQt4 import QtGui
from rissile.rio.params import model
from rissile.rio.params import delegate

class View(QtGui.QTreeView):
    """
    """
    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.clicked.connect(self.try_edit)
        self.setModel(model.Model(self))
        self.setItemDelegateForColumn(1, delegate.Delegate(self))

    def try_edit(self, index):
        if index.internalPointer().is_editable(index.column()):
            self.edit(index) 
        
    def restore_from_action(self, action):
        module = action.data().toPyObject()
        plugin = module.Plugin()
        self.model().restore_from_params(plugin.get_default_state())
        
    def generator(self):
        return self.model().generator()

