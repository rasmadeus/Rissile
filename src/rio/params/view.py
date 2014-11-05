# -*- coding: utf-8 -*-


__author__="K. Kulikov"
__date__ ="$11.07.2014 13:57:02$"


from PyQt4 import QtCore, QtGui
from rio.params import model
from rio.params import delegate

class View(QtGui.QTreeView):
    """
    Класс описывает интерфейс (является видом в паттерне MVC), который позволяет пользователю формировать входные параметры для
    исследуемого rissile.wo.WorldObjectTest. Интерфейс представлен ввиде дерева свойств вида ключ: значение.
    Модель для вида описывает класс rio.params.model
    """
    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        # Начинаем редактировать свойство по одному клику пользователя.
        self.connect(\
            self,\
            QtCore.SIGNAL('clicked(QModelIndex)'),\
            QtCore.SLOT('try_edit(QModelIndex)')\
        )        
        self.setModel(model.Model(self))
        self.setItemDelegateForColumn(1, delegate.Delegate(self)) # Второй столбец - значение свойства, подлежит редактированию.


    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def try_edit(self, index):
        if index.column() == 0: # Первый столбец - комментарий к свойству, не редактируется.
            return
        self.edit(index)
        
    def restore_from_params(self, action):
        module = action.data().toPyObject()
        plugin = module.Plugin()
        self.model().restore_from_params(plugin.get_default_state())




